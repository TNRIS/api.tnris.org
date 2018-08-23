from django.shortcuts import render
from django.http import HttpResponse
import json

from lcd import forms

def resource_update_progress(request):
    progress_tracker = forms.progress_tracker
    progress = {
       'current': progress_tracker[0],
       'total': progress_tracker[1]
    }

    data = json.dumps(progress)
    return HttpResponse(data, content_type='application/json')
