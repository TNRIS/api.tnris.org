from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from urllib.parse import urlparse
from django.conf import settings
import requests
import os, json

from .models import (
    GeneralContact
)
from .serializers import (
    GeneralContactSerializer
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
        'localhost',
        'razor-wire.tnris.org',
        'tnris.org',
        'washburn.tnris.org',
        'www.tnris.org'
    ]

    def has_permission(self, request, view):
        u = urlparse(request.META['HTTP_REFERER'])
        return u.hostname in self.whitelisted_domains

# form submission endpoint
class SubmitFormViewSet(viewsets.ViewSet):
    """
    Handle form submission
    """
    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        # if in DEBUG mode, assume local development and use localhost recaptcha secret
        # otherwise, use product account secret environment variable
        recaptcha_secret = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe' if settings.DEBUG else os.environ.get('RECAPTCHA_SECRET')
        recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_data = {'secret': recaptcha_secret, 'response': request.data['recaptcha']}
        verify_req = requests.post(url=recaptcha_verify_url, data=recaptcha_data)
        # if recaptcha verification a success, add to database
        if json.loads(verify_req.text)['success']:
            formatted = {k.lower().replace(' ', '_'): v for k, v in request.data.items()}
            serializer = GeneralContactSerializer(data=formatted)
            if serializer.is_valid():
                serializer.save()
                return Response('Form Subtmitted Successfully!', status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Recaptcha Verification Failed.', status=status.HTTP_400_BAD_REQUEST)
