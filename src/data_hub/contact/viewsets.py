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
    DataHubContactSerializer,
    DataHubOrderSerializer,
    DataHubOutsideEntityContactSerializer,
    ForumJobBoardSubmissionSerializer,
    GeneralContactSerializer,
    GeorodeoCallForPresentationsSubmissionSerializer,
    GeorodeoRegistrationSerializer,
    LakesOfTexasContactSerializer,
    OrderMapSerializer,
    PosterGallerySubmissionSerializer,
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
    # :::::SAMPLE TEMPLATE:::::
    # <<form_id (with underscores replacing dashes)>> = {
    #     'serializer': <<model serializer for saving record>>,
    #     'template': EmailTemplate.objects.get(email_template_id='<<uuid of email template to use for sending email>>'),
    #     'sendpoint': <<string 'default' to send to ticketing system, otherwise, string of form object key with email address to send to>>
    # }
    contact = {
        'serializer': GeneralContactSerializer,
        'template': EmailTemplate.objects.get(email_template_id='864e1c30-6b6e-44b9-b8f0-0b56b74aa432'),
        'sendpoint': 'default'
    }
    data_tnris_org_inquiry = {
        'serializer': DataHubContactSerializer,
        'template': EmailTemplate.objects.get(email_template_id='2c498d82-a208-4fa6-a77c-6bbb9bb67b55'),
        'sendpoint': 'default'
    }
    data_tnris_org_order = {
        'serializer': DataHubOrderSerializer,
        'template': EmailTemplate.objects.get(email_template_id='58ec6e8f-94a6-4d87-9fc9-ab6da273ff41'),
        'sendpoint': 'default'
    }
    data_tnris_org_outside_entity = {
        'serializer': DataHubOutsideEntityContactSerializer,
        'template': EmailTemplate.objects.get(email_template_id='5207ac58-9cbc-486d-bac8-7b5872a39bf9'),
        'sendpoint': 'send_to_email'
    }
    georodeocfp = {
        'serializer': GeorodeoCallForPresentationsSubmissionSerializer,
        'template': EmailTemplate.objects.get(email_template_id='eefab9df-ded0-4bb5-a798-588d5ccf1de5'),
        'sendpoint': 'default'
    }
    georodeo_regis = {
        'serializer': GeorodeoRegistrationSerializer,
        'template': EmailTemplate.objects.get(email_template_id='0374caef-91fe-4cd7-893e-b100f6d8f969'),
        'sendpoint': 'email'
    }
    google_contact = {
        'serializer': TexasImageryServiceContactSerializer,
        'template': EmailTemplate.objects.get(email_template_id='a4c815c4-08bb-4dad-a14f-6b72cc8d6171'),
        'sendpoint': 'default'
    }
    google_request = {
        'serializer': TexasImageryServiceRequestSerializer,
        'template': EmailTemplate.objects.get(email_template_id='f53fa987-f67e-4660-8173-46dbae12b40c'),
        'sendpoint': 'default'
    }
    jobboard = {
        'serializer': ForumJobBoardSubmissionSerializer,
        'template': EmailTemplate.objects.get(email_template_id='6b522cc6-91e1-447a-b6a9-b5e5cc60fd01'),
        'sendpoint': 'default'
    }
    lakes_of_texas = {
        'serializer': LakesOfTexasContactSerializer,
        'template': EmailTemplate.objects.get(email_template_id='0ba9a0e9-e2bd-4990-9151-bcbada0c9973'),
        'sendpoint': 'default'
    }
    order_map = {
        'serializer': OrderMapSerializer,
        'template': EmailTemplate.objects.get(email_template_id='dab3de9a-2fa4-410c-ac1f-845ceff5b913'),
        'sendpoint': 'default'
    }
    postergallery = {
        'serializer': PosterGallerySubmissionSerializer,
        'template': EmailTemplate.objects.get(email_template_id='3ae57e81-dd3b-4ec0-8e34-a2609579f3c9'),
        'sendpoint': 'default'
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
        # get reference dictionary for objects to complete submission
        ref = getattr(FormSubmissionReference, request.data['form_id'].replace('-', '_'))
        # if recaptcha verification a success, add to database
        if json.loads(verify_req.text)['success']:
            formatted = {k.lower().replace(' ', '_'): v for k, v in request.data.items()}
            formatted['url'] = request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META.keys() else request.META['HTTP_HOST']
            serializer = ref['serializer'](data=formatted)
            if serializer.is_valid():
                serializer.save()
                body = self.compile_email_body(ref['template'].email_template_body, formatted)
                # send to ticketing system unless sendpoint has alternative key value in ref
                sender = os.environ.get('MAIL_DEFAULT_TO') if ref['sendpoint'] == 'default' else formatted[ref['sendpoint']]
                self.send_email(ref['template'].email_template_subject, body, send_to=sender, reply_to=formatted['email'])
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
