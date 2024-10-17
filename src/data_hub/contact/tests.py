import requests
import os
from django import http
from django.core import mail
from django.test import TestCase, Client, AsyncRequestFactory
from contact.viewsets import SubmitFormViewSet
from contact.new_contacts import SubmitFormViewSetSuper
from .models import EmailTemplate, OrderType, OrderDetailsType
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

class NewContactsTestCase(TestCase):
    """Test that recaptcha blocks us when we access it without a captcha."""        
    fixtures = ['testapi.json']

    def test_submit_form_blocking(self):
        """Test the payment portal blocks failed captchas."""
        request = requests.Request(method='POST', data={"recaptcha": "none"})

        submit_form = SubmitFormViewSet()
        response = submit_form.create(request)
        self.assertEquals(response.status_code, 400, "SubmitForm not blocking failed captchas correctly, and status code is not 400.")

    def test_submit_form(self):
        """Test that submit form super class functions correctly."""
        submit_form_super = SubmitFormViewSetSuper()
        req_factory = AsyncRequestFactory()

        request = req_factory.post(
            data={
                "recaptcha": "none",
                "form_id": "data-tnris-org-order"
            },
            content_type='application/json',
            headers={
                "Referer": "localhost"
            },
            path="contact/order/submit/",
        )
        request = Request(request, parsers=[JSONParser()])
        response = submit_form_super.create(request)

        # Make sure we get a 201 created response.
        self.assertEquals(response.status_code, 201, "Form submission was not successful.")

        # Make sure email is sent.
        self.assertEqual(len(mail.outbox), 1, "No email has been sent.")

    def test_payment_portal(self):
        """Test data cleanup."""
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
