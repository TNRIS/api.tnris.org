from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from django.utils.translation import gettext as _

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


def server_error(request):
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


def csrf_failure(request, reason="", template_name='data_hub/403_csrf.html'):
    """
    Custom view to use when request fails CSRF protection
    """
    from django.middleware.csrf import REASON_NO_CSRF_COOKIE, REASON_NO_REFERER
    context = {
        'title': _("Forbidden"),
        'main': _("CSRF verification failed. Request aborted."),
        'reason': reason,
        'no_referer': reason == REASON_NO_REFERER,
        'no_referer1': _(
            'You are seeing this message because this HTTPS site requires a '
            '“Referer header” to be sent by your Web browser, but none was '
            'sent. This header is required for security reasons, to ensure '
            'that your browser is not being hijacked by third parties.'),
        'no_referer2': _(
            'If you have configured your browser to disable “Referer” headers, '
            'please re-enable them, at least for this site, or for HTTPS '
            'connections, or for “same-origin” requests.'),
        'no_referer3': _(
            'If you are using the <meta name="referrer" '
            'content=\"no-referrer\"> tag or including the “Referrer-Policy: '
            'no-referrer” header, please remove them. The CSRF protection '
            'requires the “Referer” header to do strict referer checking. If '
            'you’re concerned about privacy, use alternatives like '
            '<a rel=\"noreferrer\" …> for links to third-party sites.'),
        'no_cookie': reason == REASON_NO_CSRF_COOKIE,
        'no_cookie1': _(
            "You are seeing this message because this site requires a CSRF "
            "cookie when submitting forms. This cookie is required for "
            "security reasons, to ensure that your browser is not being "
            "hijacked by third parties."),
        'no_cookie2': _(
            'If you have configured your browser to disable cookies, please '
            're-enable them, at least for this site, or for “same-origin” '
            'requests.'),
    }
    response = render(request, template_name, context)
    response.status_code = 403
    return response
