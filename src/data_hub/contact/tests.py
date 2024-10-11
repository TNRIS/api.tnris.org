import requests
import os
from django import http
from django.test import TestCase
from contact.viewsets import SubmitFormViewSet
from contact.new_contacts import SubmitFormViewSetSuper

# Create your tests here.
class ShopTestCase(TestCase):
    """Test for the Payment portal."""
    def test_payment_portal(self):
        """Test the payment portal."""

        # The API endpoint
        url = "http://localhost:8000/api/v1/contact/order/retentionCleanup"

        # Data to be sent
        # If approve_run is false then only tests will be ran.
        data = {
            "access_code": os.environ.get("CCP_ACCESS_CODE"),
            "approve_run": "false"
        }

        # A POST request to the API
        response = requests.post(url, json=data, timeout=10)
        res = response.json()
        if 'orders_to_be_archived' in res:
            self.assertIsNotNone(res['orders_to_be_archived'], "SUCCESS: orders to be archived is not none.")

        if 'orders_to_be_deleted' in res:
            self.assertIsNotNone(res['orders_to_be_deleted'], "SUCCESS: orders to be deleted is not none.")

class SubmitFormBlockRecaptchaFailureTestCase(TestCase):
    """Test that recaptcha blocks us when we access it without a captcha."""
    def test_submit_form(self):
        """Test the payment portal blocks failed captchas."""
        request = requests.Request(method='POST', data={"recaptcha": "none"})

        submit_form = SubmitFormViewSet()
        response = submit_form.create(request)
        self.assertEquals(response.status_code, 400, "SubmitForm not blocking failed captchas correctly, and status code is not 400.")

class SubmitFormSuperTestCase(TestCase):
    """Test that submit form super class functions correctly."""
    def test_submit_form(self):
        """Test that submit form super class functions correctly."""
        submit_form_super = SubmitFormViewSetSuper()
        request = requests.Request(method='POST', data={"recaptcha": "none"})

        response = submit_form_super.create(request)
