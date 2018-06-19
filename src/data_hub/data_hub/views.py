from django.http import HttpResponse
from django.views.generic import View


class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=200)
        
