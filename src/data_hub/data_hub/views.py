from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("hi there", status=200)

"""
error code handling
"""

def bad_request(request, exception):
    context = {
        'status': 400,
        'text': 'Bad Request'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 400
    return response


def permission_denied(request, exception):
    context = {
        'status': 403,
        'text': 'Permission Denied'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 403
    return response


def page_not_found(request, exception):
    context = {
        'status': 404,
        'text': 'Page Not Found'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 404
    return response


def server_error(request, exception):
    context = {
        'status': 500,
        'text': 'Server Error'
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 500
    return response