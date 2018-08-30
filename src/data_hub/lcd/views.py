from django.shortcuts import render
from django.http import HttpResponse
import json

from lcd import forms

# this route is normally called to manage the progress bar on the Add Resource
# admin form but is not used in production because the forms global variable
# "progress_tracker" does not update during Save() when deployed. Works locally though
def resource_update_progress(request):
    progress_tracker = forms.progress_tracker
    progress = {
       'current': progress_tracker[0],
       'total': progress_tracker[1]
    }

    data = json.dumps(progress)
    return HttpResponse(data, content_type='application/json')
