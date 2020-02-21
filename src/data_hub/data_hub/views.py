from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from lcd.models import Quote
import random


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("hi there", status=200)

"""
error code handling
"""

def random_rec():
    count = Quote.objects.all().count()
    random_index = random.randint(0, count - 1)
    return Quote.objects.all()[random_index]


def bad_request(request, exception):
    q = random_rec()
    context = {
        'status': 400,
        'text': 'Bad Request',
        'author': q.author,
        'quote': q.quote
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 400
    return response


def permission_denied(request, exception):
    q = random_rec()
    context = {
        'status': 403,
        'text': 'Permission Denied',
        'author': q.author,
        'quote': q.quote
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 403
    return response


def page_not_found(request, exception):
    q = random_rec()
    context = {
        'status': 404,
        'text': 'Page Not Found',
        'author': q.author,
        'quote': q.quote
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 404
    return response


def server_error(request, exception):
    q = random_rec()
    context = {
        'status': 500,
        'text': 'Server Error',
        'author': q.author,
        'quote': q.quote
    }
    response = render(request, 'data_hub/error.html', context)
    response.status_code = 500
    return response
