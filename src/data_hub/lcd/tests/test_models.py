import datetime

from django.test import TestCase
from django.utils import timezone

from .models import *
# import AreaType, CategoryType, EpsgType, FileType, LicenseType, ResolutionType, ResourceType, SourceType, TemplateType,

# Create your tests here.

class ModelDateTests(TestCase):

    def test_for_future_dates(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        print("checking for future dates...")
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = AreaType(created=time)
        self.assertIs(future_question.was_published_recently(), False)
