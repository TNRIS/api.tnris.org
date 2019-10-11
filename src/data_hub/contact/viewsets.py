from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import EmailMessage
import requests, os, json, re, datetime, base64, hmac, hashlib, sys

from .models import (
    EmailTemplate
)

from .serializers import *

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
            injected = injected.replace(var, str(dict[k]))
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
        # this 'if' clause is temporary. a fix for lake-gallery issue 139.
        # after recaptcha is added to the lakes of texas frontend form, this
        # if/else can go away and the """response: request.data['recaptcha']""" 
        # should be used for all forms.
        if request.data['form_id'] != 'lakes-of-texas':
            recaptcha_data = {'secret': recaptcha_secret, 'response': request.data['recaptcha']}
        else:
            recaptcha_data = {'secret': recaptcha_secret, 'response': 'lakesoftexasform'}
        verify_req = requests.post(url=recaptcha_verify_url, data=recaptcha_data)
        # get email template for form. if bad form, return error
        try:
            email_template = EmailTemplate.objects.get(form_id=request.data['form_id'])
        except:
            return Response({
                    'status': 'error',
                    'message': 'form_id not registered.'
                }, status=status.HTTP_400_BAD_REQUEST)
        # if recaptcha verification a success, add to database
        if json.loads(verify_req.text)['success']:
            formatted = {k.lower().replace(' ', '_'): v for k, v in request.data.items()}
            formatted['url'] = request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META.keys() else request.META['HTTP_HOST']
            serializer = getattr(sys.modules[__name__], email_template.serializer_classname)(data=formatted)
            if serializer.is_valid():
                serializer.save()
                body = self.compile_email_body(email_template.email_template_body, formatted)
                # send to ticketing system unless sendpoint has alternative key value in email template record
                sender = os.environ.get('MAIL_DEFAULT_TO') if email_template.sendpoint == 'default' else formatted[email_template.sendpoint]
                replyer = formatted['email'] if 'email' in formatted.keys() else ''
                self.send_email(email_template.email_template_subject, body, send_to=sender, reply_to=replyer)
                return Response({
                        'status': 'success',
                        'message': 'Form Submitted Successfully!'
                    }, status=status.HTTP_201_CREATED)
            return Response({
                    'status': 'error',
                    'message': 'Serializer Save Failed.',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                    'status': 'error',
                    'message': 'Recaptcha Verification Failed.'
                }, status=status.HTTP_400_BAD_REQUEST)


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
