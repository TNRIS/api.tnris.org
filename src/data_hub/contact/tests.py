import requests
import os
from django import http
from django.core import mail
from django.test import TestCase, Client, AsyncRequestFactory
from contact.viewsets import SubmitFormViewSet, GenOtpViewSet, OrderSubmitViewSet, OrderFormViewSet
from contact.new_contacts import GenOtpViewSetSuper, OrderSubmitViewSetSuper, OrderFormViewSetSuper
from .models import EmailTemplate, OrderType, OrderDetailsType
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

def create_super_request(data):
    """Build a request that calls the super classes directly"""
    req_factory = AsyncRequestFactory()
    request = req_factory.post(
        data=data,
        content_type='application/json',
        headers={
            "Referer": "localhost"
        },
        path="none"
    )
    # Convert to a plain request that is used by Django. Then return it
    return Request(request, parsers=[JSONParser()])

class OrderFormTestCase(TestCase):
    """Test Order Form Submission"""
    fixtures = ['testapi.json']

    def test_order_form_blocking(self):
        """Test the order form submit blocks failed captchas."""
        request = requests.Request(method='POST', data={"recaptcha": "none"})
        order_form = OrderFormViewSet()
        response = order_form.create(request)
        self.assertEquals(response.status_code, 403, "Order submit route not sending 403 Forbidden signal.")

    def test_order_submit(self):
        """Test Order Submit create function"""
        order_form_super = OrderFormViewSetSuper()
        request = create_super_request({
            "recaptcha": "none",
            "form_id": "data-tnris-org-order",
            "order_details": {
                "item": 50,
            },
            "EMAIL": os.environ.get("MAIL_DEFAULT_TO") #Caps to test that route makes keys lowercase

        })
        response = order_form_super.create(request)
        
        # Make sure we get a 201 created response.
        self.assertEquals(response.status_code, 201, "Form submission was not successful.")

        # Expected two emails to be sent. 
        self.assertEqual(len(mail.outbox), 2, "No email has been sent.")
        
    def test_order_map(self):
        """Test ordering of map"""
        order_form_super = OrderFormViewSetSuper()
        request = create_super_request({
            "recaptcha": "none",
            "form_id": "order-map",
            "order_details": {
                "item": 50
            },
            "EMAIL": os.environ.get("MAIL_DEFAULT_TO") #Caps to test that route makes keys lowercase
        })
        response = order_form_super.create(request)

        # Make sure we get a 201 created response.
        self.assertEquals(response.status_code, 201, "Form submission was not successful.")

        # Expected two emails to be sent. 
        self.assertEqual(len(mail.outbox), 2, "No email has been sent.")


class GoneTestCase(TestCase):
    """Test that old order urls are gone."""
    def test_gone(self):
        """Test that old order urls are gone."""
        request = requests.Request(method='POST', data={"recaptcha": "none"})

        submit_form = SubmitFormViewSet()
        response = submit_form.create(request)
        self.assertEquals(response.status_code, 410, "Submit route not sending 410 GONE signal.")

class GenOtpTestCase(TestCase):
    """Test OTP."""        
    fixtures = ['testapi.json']

    def test_gen_otp_form_blocking(self):
        """Test the OTP blocks failed captchas."""
        request = requests.Request(method='POST', data={"recaptcha": "none"})

        genotp_form = GenOtpViewSet()
        response = genotp_form.create(request)
        self.assertEquals(response.status_code, 403, "GenOtp not blocking failed captchas correctly, and status code is not 400.")

    # def gen_otp(self):
    #     """Test that submit form super class functions correctly."""
    #     submit_form_super = GenOtpViewSetSuper()
    #     req_factory = AsyncRequestFactory()

    #     request = req_factory.post(
    #         data={
    #             "recaptcha": "none",
    #             "form_id": "data-tnris-org-order"
    #         },
    #         content_type='application/json',
    #         headers={
    #             "Referer": "localhost"
    #         },
    #         path="contact/order/submit/",
    #     )
    #     request = Request(request, parsers=[JSONParser()])
    #     response = submit_form_super.create(request)

    #     # # Make sure we get a 201 created response.
    #     # self.assertEquals(response.status_code, 201, "Form submission was not successful.")

    #     # # Make sure email is sent.
    #     # self.assertEqual(len(mail.outbox), 1, "No email has been sent.")

    # def test_payment_portal(self):
    #     """Test data cleanup."""
    #     # The API endpoint
    #     url = "http://localhost:8000/api/v1/contact/order/retentionCleanup"

    #     # Data to be sent
    #     # If approve_run is false then only tests will be ran.
    #     data = {
    #         "access_code": os.environ.get("CCP_ACCESS_CODE"),
    #         "approve_run": "false"
    #     }

    #     # A POST request to the API
    #     response = requests.post(url, json=data, timeout=10)
    #     res = response.json()
    #     if 'orders_to_be_archived' in res:
    #         self.assertIsNotNone(res['orders_to_be_archived'], "SUCCESS: orders to be archived is not none.")

    #     if 'orders_to_be_deleted' in res:
    #         self.assertIsNotNone(res['orders_to_be_deleted'], "SUCCESS: orders to be deleted is not none.")

class OrderSubmitTestCase(TestCase):
    """Test Order Submit"""
    def test_gen_order_submit_blocking(self):
        """Test the order submit blocks failed captchas."""
        request = requests.Request(method='POST', data={"recaptcha": "none"})
        order_submit = OrderSubmitViewSet()
        response = order_submit.create(request)
        self.assertEquals(response.status_code, 403, "Order submit route not sending 403 Forbidden signal.")

    def test_order_submit(self):
        """Test Order Submit create function"""
        submit_form_super = OrderSubmitViewSetSuper()
        request = create_super_request({
            "recaptcha": "none",
            "form_id": "data-tnris-org-order"
        })
        #response = submit_form_super.create(request)

        # # Make sure we get a 201 created response.
        # self.assertEquals(response.status_code, 201, "Form submission was not successful.")

        # # Make sure email is sent.
        # self.assertEqual(len(mail.outbox), 1, "No email has been sent.")