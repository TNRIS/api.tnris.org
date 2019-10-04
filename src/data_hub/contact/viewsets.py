from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import EmailMessage
import requests, os, json, re, datetime, base64, hmac, hashlib

from .models import (
    EmailTemplate
)
from .serializers import (
    GeneralContactSerializer,
    TexasImageryServiceContactSerializer,
    TexasImageryServiceRequestSerializer
)

# custom permissions for cors control
class CorsPostPermission(AllowAny):
    whitelisted_domains = [
        'beta.tnris.org',
        'data.tnris.org',
        'ellwood.tnris.org',
        'frye.tnris.org',
        'glidden.tnris.org',
        'haish.tnris.org',
        'lake-gallery.tnris.org',
        'localhost:8000',
        'localhost:8020',
        'localhost:3000',
        'razor-wire.tnris.org',
        'tnris.org',
        'washburn.tnris.org',
        'www.tnris.org'
    ]

    def has_permission(self, request, view):
        u = request.META['HTTP_HOST']
        return u in self.whitelisted_domains


# template-to-model relationship reference.
# would be best if could be stored in database table, but saving model
# objects as field values is not obvious
class FormSubmissionReference:
    contact = {
        'serializer': GeneralContactSerializer,
        'template': EmailTemplate.objects.get(email_template_id='864e1c30-6b6e-44b9-b8f0-0b56b74aa432')
    }
    google_contact = {
        'serializer': TexasImageryServiceContactSerializer,
        'template': EmailTemplate.objects.get(email_template_id='a4c815c4-08bb-4dad-a14f-6b72cc8d6171')
    }
    google_request = {
        'serializer': TexasImageryServiceRequestSerializer,
        'template': EmailTemplate.objects.get(email_template_id='f53fa987-f67e-4660-8173-46dbae12b40c')
    }


# form submission endpoint
class SubmitFormViewSet(viewsets.ViewSet):
    """
    Handle form submission
    """
    permission_classes = [CorsPostPermission]

    # inject form values into email template body
    def compile_email_body(self, template_body, dict):
        injected = template_body
        # loop form value keys and replace in template
        for k in dict.keys():
            var = "{{%s}}" % k
            injected = injected.replace(var, dict[k])
        # replace all template values which weren't in the form (optional form fields)
        injected = re.sub(r'\{\{.*?\}\}', '', injected)
        return injected

    # generic function for sending email associated with form submission
    # emails send to supportsystem to create tickets in the ticketing system
    # which are ultimately managed by IS, RDC, and StratMap
    def send_email(self,
                   subject,
                   body,
                   send_from=os.environ.get('MAIL_DEFAULT_FROM'),
                   send_to=os.environ.get('MAIL_DEFAULT_TO'),
                   send_bcc=os.environ.get('MAIL_DEFAULT_FROM'),
                   reply_to='unknown@tnris.org'):
        email = EmailMessage(
                    subject,
                    body,
                    send_from,
                    [send_to],
                    [send_bcc],
                    reply_to=[reply_to]
                )
        email.send(fail_silently=False)
        return


    def create(self, request, format=None):
        # if in DEBUG mode, assume local development and use localhost recaptcha secret
        # otherwise, use product account secret environment variable
        recaptcha_secret = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe' if settings.DEBUG else os.environ.get('RECAPTCHA_SECRET')
        recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {'secret': recaptcha_secret, 'response': request.data['recaptcha']}
        verify_req = requests.post(url=recaptcha_verify_url, data=recaptcha_data)
        # get reference dictionary for objects to complete submission
        ref = getattr(FormSubmissionReference, request.data['form_id'].replace('-', '_'))
        # if recaptcha verification a success, add to database
        if json.loads(verify_req.text)['success']:
            formatted = {k.lower().replace(' ', '_'): v for k, v in request.data.items()}
            formatted['url'] = request.META['HTTP_HOST']
            serializer = ref['serializer'](data=formatted)
            if serializer.is_valid():
                serializer.save()
                body = self.compile_email_body(ref['template'].email_template_body, formatted)
                self.send_email(ref['template'].email_template_subject, body, reply_to=formatted['email'])
                return Response('Form Submitted Successfully!', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Recaptcha Verification Failed.', status=status.HTTP_400_BAD_REQUEST)


# POLICY ENDPOINTS
def default_policy_opts(length, content_type):
    # setup options needed to create signature
    bucket = os.environ.get('S3_UPLOAD_BUCKET')
    secret = os.environ.get('S3_UPLOAD_SECRET')
    key = os.environ.get('S3_UPLOAD_KEY')
    # create time string in UTC zulu time. expire signature in 15 minutes
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    expires_formatted = expires.isoformat(timespec='milliseconds') + 'Z'
    opts = {
        'length': length,
        'type': content_type,
        'expires': expires_formatted,
        'bucket': bucket,
        'secret': secret,
        'key': key,
        'acl': 'private',
        'conditions': [
            ['starts-with', '$success_action_status', ''],
            ['starts-with', '$success_action_redirect', ''],
            ['starts-with', '$key', ''],
            ['starts-with', '$Content-Type', content_type],
            ['starts-with', '$Content-Length', ''],
            ['content-length-range', 1, length]
        ]
    }
    return opts

def build_signed_policy(opts):
    # create base64 policy
    con = opts['conditions']
    ext = [{'bucket': opts['bucket']}, {'acl': opts['acl']}]
    con.extend(ext)
    policy_data = {
        'expiration': opts['expires'],
        'conditions': con
    }
    # convert json of policy parameters into string and encode
    dumped = json.dumps(policy_data)
    encoded = base64.b64encode(dumped.encode("utf-8"))
    # create hash signature
    m = hmac.new(opts['secret'].encode("utf-8"), encoded, hashlib.sha1).digest()
    hashed = base64.b64encode(m)
    signed_policy = {
        'policy': encoded,
        'signature': hashed,
        'key': opts['key']
    }
    return signed_policy


class ZipPolicyViewSet(viewsets.ViewSet):
    """
    Get zipfile upload policy for s3
    """
    permission_classes = [CorsPostPermission]

    def list(self, request, format=None):
        try:
            opts = default_policy_opts(20971520, 'application/zip') # 20MB
            signed_policy = build_signed_policy(opts)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(signed_policy, status=status.HTTP_201_CREATED)


class ImagePolicyViewSet(viewsets.ViewSet):
    """
    Get image upload policy for s3
    """
    permission_classes = [CorsPostPermission]

    def list(self, request, format=None):
        try:
            opts = default_policy_opts(5242880, 'image') # 5MB
            signed_policy = build_signed_policy(opts)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(signed_policy, status=status.HTTP_201_CREATED)


class FilePolicyViewSet(viewsets.ViewSet):
    """
    Get generic file upload policy for s3
    """
    permission_classes = [CorsPostPermission]

    def list(self, request, format=None):
        try:
            opts = default_policy_opts(5242880, '') # 5MB
            signed_policy = build_signed_policy(opts)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(signed_policy, status=status.HTTP_201_CREATED)
