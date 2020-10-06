from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from urllib.parse import urlparse
from django.conf import settings
from django.core.mail import EmailMessage
import requests, os, json, re, sys
# policy imports
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config

from .models import (
    EmailTemplate,
    SurveyTemplate
)

from .serializers import *

# custom permissions for cors control
class CorsPostPermission(AllowAny):
    whitelisted_domains = [
        'api.tnris.org',
        'beta.tnris.org',
        'data.tnris.org',
        'develop.tnris.org',
        'lake-gallery.tnris.org',
        'localhost:8000',
        'localhost',
        'staging.tnris.org',
        'tnris.org',
        'www.tnris.org'
    ]

    def has_permission(self, request, view):
        u = urlparse(request.META['HTTP_REFERER']).hostname if 'HTTP_REFERER' in request.META.keys() else request.META['HTTP_HOST']
        return u in self.whitelisted_domains


# form submission endpoint
class SubmitFormViewSet(viewsets.ViewSet):
    """
    Handle TNRIS form submissions (Restricted Access)
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
                   reply_to='unknown@tnris.org'):
        email = EmailMessage(
                    subject,
                    body,
                    send_from,
                    [send_to],
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
                replyer = formatted['email'] if 'email' in formatted.keys() else 'unknown@tnris.org'
                if 'name' in formatted.keys():
                    replyer = '%s <%s>' % (formatted['name'], formatted['email'])
                elif 'firstname' in formatted.keys() and 'lastname' in formatted.keys():
                    replyer = '%s %s <%s>' % (formatted['firstname'], formatted['lastname'], formatted['email'])
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
def create_presigned_post(key, content_type, length, expiration=900):
    """Generate a presigned URL S3 POST request to upload a file

    :param key: string
    :param content_type: string
    :param length: integer
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid. default 15min
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    bucket = os.environ.get('S3_UPLOAD_BUCKET')
    fields = {
        'acl': 'private',
        'Content-Type': content_type,
        'Content-Length': length,
        'success_action_status': '201',
        'success_action_redirect': ''
    }
    # if in conditions array, must be in fields dictionary and client
    # side form inputs/fields as well
    conditions = [
            {'acl':'private'},
            ['starts-with', '$success_action_status', ''],
            ['starts-with', '$success_action_redirect', ''],
            ['starts-with', '$key', ''],
            ['starts-with', '$Content-Type', content_type],
            ['starts-with', '$Content-Length', ''],
            ['content-length-range', 1, length]
        ]
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3',
        aws_access_key_id=os.environ.get('S3_UPLOAD_KEY'),
        aws_secret_access_key=os.environ.get('S3_UPLOAD_SECRET'),
        config=Config(signature_version='s3v4')
    )
    try:
        response = s3_client.generate_presigned_post(bucket,
                                                     key,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


class ZipPolicyViewSet(viewsets.ViewSet):
    """
    Get client form zipfile presigned url for s3 (Restricted Access)
    """
    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            presigned = create_presigned_post(request.data['key'], 'application/zip', 20971520)  # 20MB
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(presigned, status=status.HTTP_201_CREATED)


class ImagePolicyViewSet(viewsets.ViewSet):
    """
    Get client form image presigned url for s3 (Restricted Access)
    """
    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            presigned = create_presigned_post(request.data['key'], 'image', 5242880)  # 5MB
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(presigned, status=status.HTTP_201_CREATED)


class FilePolicyViewSet(viewsets.ViewSet):
    """
    Get client form generic file presigned url for s3 (Restricted Access)
    """
    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            presigned = create_presigned_post(request.data['key'], '', 5242880)  # 5MB
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(presigned, status=status.HTTP_201_CREATED)


class SurveyTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve surveys to deliver survey modal content to front-end
    """
    serializer_class = SurveyTemplateSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # only return latest public survey record
        args = {'public': True}
        
        # get records using query
        queryset = SurveyTemplate.objects.filter(**args).order_by('-last_modified')
        return queryset