from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("hi there", status=200)

"""
error code handling
"""

def bad_request(request):
    context = {
        'code': 400,
        'text': 'Bad Request',
        'key': 'hulk.png'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 400
    return response


def permission_denied(request):
    context = {
        'code': 403,
        'text': 'Permission Denied',
        'key': 'flair.png'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 403
    return response


def page_not_found(request):
    context = {
        'code': 404,
        'text': 'Page Not Found',
        'key': 'giant.png'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 404
    return response


def server_error(request):
    context = {
        'code': 500,
        'text': 'Server Error',
        'key': 'macho.png'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 500
    return response