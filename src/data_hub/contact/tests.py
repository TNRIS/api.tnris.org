from urllib import request
import requests
import os
import json
from django.core import mail
from django.test import TestCase, AsyncRequestFactory
from contact.viewsets import (
    GenOtpViewSet,
    SubmitFormViewSet,
    OrderSubmitViewSet,
    OrderFormViewSet,
    InitiateRetentionCleanupViewSet,
    OrderCleanupViewSet
)
from contact.new_contacts import (
    GenOtpViewSetSuper,
    OrderFormViewSetSuper,
    OrderSubmitViewSetSuper,
    OrderStatusViewSetSuper,
    InitiateRetentionCleanupViewSetSuper,
    OrderCleanupViewSetSuper
)
from .models import OrderType
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from modules import api_helper

from contact.constants import payload_valid_test

FISERV_URL = "https://snappaydirectapi-cert.fiserv.com/api/interop/v2/"


def create_super_request(data, query_params=""):
    """Build a request that calls the super classes directly"""
    req_factory = AsyncRequestFactory()
    request = req_factory.post(
        data=data,
        content_type="application/json",
        headers={"Referer": "localhost"},
        path="none{}".format(query_params),
    )

    # Convert to a plain request that is used by Django. Then return it
    django_request = Request(request, parsers=[JSONParser()])
    return django_request


class GeneralTest(TestCase):
    """Inheritable with some common setup."""

    fixtures = ["email_templates.json"]
    uuid = ""
    order_details_new = {
        "Name": "FIRSTNAME LASTNAME",
        "Email": "TxGIO-DevOps@twdb.texas.gov",
        "Phone": "1112223333",
        "Address": "State Parking Garage E",
        "City": "Austin",
        "State": "Texas",
        "Zipcode": "78660",
        "Organization": "TEST",
        "Industry": "TESTING",
        "Fedex": "",
        "Notes": "Test Note",
        "Delivery": "Test Delivery",
        "HardDrive": "Test Hard Drive",
        "Payment": "CC",
        "Order": "Test item 1\nTest Item 2",
        "form_id": "data-tnris-org-order",
    }

    def setUp(self):
        order = OrderFormViewSetSuper.create_order_object(
            self,
            email="TxGIO-DevOps@twdb.texas.gov",
            order_details=self.order_details_new,
            test_otp="12345",
        )
        order.order_approved = True
        order.approved_charge = 7.0
        order.save()
        self.uuid = str(order.id)
        # # Make sure email is sent.
        self.assertEqual(
            len(mail.outbox), 1, "No email has been sent. in GeneralTest.setup()"
        )

class OrderCleanupTestCase(GeneralTest): # Tested done pt1.
    """Order cleanup test case."""

    def test_order_cleanup(self):
        order_cleanup = OrderCleanupViewSetSuper()
        request = create_super_request(
            {"access_code": os.environ.get("CCP_ACCESS_CODE")}
        )
        response = order_cleanup.create(request)

        print("Break")

class InitiateRetentionCleanupTestCase(GeneralTest):  # Tested done pt1.
    """Initiate retention cleanup test case."""

    def test_initiate_retentions_cleanup(self):
        initiate_cleanup = InitiateRetentionCleanupViewSetSuper()
        request = create_super_request(
            {"approve_run": "none", "access_code": os.environ.get("CCP_ACCESS_CODE")}
        )
        response = initiate_cleanup.create(request)
        self.assertEquals(response.status_code, 200, "Order status successful.")


class OrderStatusTestCase(GeneralTest):  # Tested done pt1.
    """Query Fiserv for order status"""

    def test_order_status(self):
        """Test getting order status"""
        order_status_super = OrderStatusViewSetSuper()
        request = create_super_request(
            {
                "recaptcha": "none",
                "accessCode": "TxGIO-DevOps@twdb.texas.gov",
                "form_id": "order-map",
                "EMAIL": os.environ.get(
                    "MAIL_DEFAULT_TO"
                ),  # Caps to test that route makes keys lowercase
                "passCode": "12345",  # Note: this is not a real passcode.
            },
            f"?uuid={self.uuid}",
        )
        response = order_status_super.create(request)

        # Make sure we get a 200 created response.
        self.assertEquals(response.status_code, 200, "Order status unsuccessful.")


class OrderFormTestCase(TestCase):  # Tested done pt1.
    """Test Order Form Submission"""

    fixtures = ["email_templates.json"]

    def test_order_form_blocking(self):
        """Test the order form submit blocks failed captchas."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})
        order_form = OrderFormViewSet()
        response = order_form.create(request)
        self.assertEquals(
            response.status_code,
            403,
            "Order submit route not sending 403 Forbidden signal.",
        )

    def test_order_submit(self):
        """Test Order Submit create function"""
        order_form_super = OrderFormViewSetSuper()
        request = create_super_request(
            {
                "recaptcha": "none",
                "form_id": "data-tnris-org-order",
                "order_details": {"item": 50, "PAYMENT": 5.42},
                "EMAIL": os.environ.get(
                    "MAIL_DEFAULT_TO"
                ),  # Caps to test that route makes keys lowercase
            }
        )
        response = order_form_super.create(request)

        # Make sure order was submitted and created successfully.
        orders = OrderType.objects.get_queryset()
        if len(orders):  # Check there is an item
            order = orders[0]

            # TODO Check each item instead of all at once
            self.assertIsNotNone(order, "Items does not exist")

            # Make sure order details was created successfully.
            order_details = order.order_details
            self.assertIsNotNone(order_details, "Item Details does not exist")

            # Make sure we get a 201 created response.
            self.assertEquals(
                response.status_code, 201, "Form submission was not successful."
            )
        else:
            self.fail("No order was created.")

        # Expected two emails to be sent.
        self.assertEqual(len(mail.outbox), 2, "No email has been sent.")

    def test_order_map(self):
        """Test ordering of map"""
        order_form_super = OrderFormViewSetSuper()
        request = create_super_request(
            {
                "recaptcha": "none",
                "form_id": "order-map",
                "order_details": {"item": 50, "PAYMENT": 5.43},
                "EMAIL": os.environ.get(
                    "MAIL_DEFAULT_TO"
                ),  # Caps to test that route makes keys lowercase
            }
        )
        response = order_form_super.create(request)

        # Make sure we get a 201 created response.
        self.assertEquals(
            response.status_code, 201, "Form submission was not successful."
        )

        # Expected two emails to be sent.
        self.assertEqual(len(mail.outbox), 2, "No email has been sent.")


class GoneTestCase(TestCase):  # Tested done pt1.
    """Test that old order urls are gone."""

    def test_gone(self):
        """Test that old order urls are gone."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})

        submit_form = SubmitFormViewSet()
        response = submit_form.create(request)
        self.assertEquals(
            response.status_code, 410, "Submit route not sending 410 GONE signal."
        )


class GenOtpTestCase(GeneralTest):  # Tested done pt1.
    """Test OTP."""

    def test_gen_otp_form_blocking(self):
        """Test the OTP blocks failed captchas."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})

        # build a basic request to test with
        request = create_super_request({"recaptcha": "none"}, f"?uuid={self.uuid}")

        genotp_form = GenOtpViewSet()
        response = genotp_form.create(request)

        self.assertEquals(
            response.status_code,
            403,
            "Generate OTP route not sending 403 Forbidden signal.",
        )

    def test_gen_otp(self):
        """Test the OTP generation process."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})

        # build a basic request to test with
        request = create_super_request({"recaptcha": "none"}, f"?uuid={self.uuid}")

        genotp_form = GenOtpViewSetSuper()
        response = genotp_form.create(request)
        self.assertEquals(
            response.status_code,
            200,
            "Test the OTP generation failed.",
        )

        self.assertEquals(
            response.data["status"],
            "success",
            "Test the OTP generation failed.",
        )
        print("Breakpoint test")


class OrderSubmitTestCase(GeneralTest):  # Tested done pt1.
    """Test Order Submit"""

    def test_gen_order_submit_blocking(self):
        """Test the order submit blocks failed captchas."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})
        order_submit = OrderSubmitViewSet()
        response = order_submit.create(request)
        self.assertEquals(
            response.status_code,
            403,
            "Order submit route not sending 403 Forbidden signal.",
        )

    def test_order_submit(self):
        """Test creating HPP Link"""
        submit_form_super = OrderSubmitViewSetSuper()
        request = create_super_request(
            {
                "recaptcha": "none",
                "form_id": "data-tnris-org-order",
                "accessCode": "TxGIO-DevOps@twdb.texas.gov",
                "passCode": "12345",  # Note: this is not a real passcode.
            },
            f"?uuid={self.uuid}",
        )
        response = submit_form_super.create(request)

        # # Make sure we get a 201 created response.
        self.assertEquals(
            response.status_code, 200, "Form submission and HPP was not created."
        )


class FiservTestCase(TestCase):  # Tested done pt1.
    """Test Fiserv endpoints"""

    def test_make_hmac(self):
        requestUri: str = f"{FISERV_URL}GetRequestID"
        hmac = api_helper.generate_fiserv_hmac(
            requestUri,
            "POST",
            json.dumps(payload_valid_test),
            os.environ.get("FISERV_DEV_ACCOUNT_ID"),
            os.environ.get("FISERV_DEV_AUTH_CODE"),
        )
        self.assertIsNotNone(hmac)
        basic = api_helper.generate_basic_auth()
        response = requests.post(
            FISERV_URL + "GetRequestID",
            json=payload_valid_test,
            headers={
                "accountid": os.environ.get("FISERV_DEV_ACCOUNT_ID"),  # good
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),  # good
                "signature": f"Hmac {hmac.decode()}",
                "Authorization": f"Basic {basic.decode()}",
            },
        )

        self.assertIs(response.status_code, 200, "response status_code is not 200")
        print(
            "Error: "
            + str(response.status_code)
            + " "
            + json.loads(response.text)["message"]
        )
