import requests
import os
from django.core import mail
from django.test import TestCase, AsyncRequestFactory
from contact.viewsets import (
    SubmitFormViewSet,
    OrderSubmitViewSet,
    OrderFormViewSet,
)
from contact.new_contacts import (
    GenOtpViewSetSuper,
    OrderSubmitViewSetSuper,
    OrderFormViewSetSuper,
)
from .models import EmailTemplate, OrderType, OrderDetailsType
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from modules import api_helper

FISERV_URL = "https://snappaydirectapi-cert.fiserv.com/api/interop/"


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


class OrderFormTestCase(TestCase):
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
                "order_details": {
                    "item": 50,
                },
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
                "order_details": {"item": 50},
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


class GoneTestCase(TestCase):
    """Test that old order urls are gone."""

    def test_gone(self):
        """Test that old order urls are gone."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})

        submit_form = SubmitFormViewSet()
        response = submit_form.create(request)
        self.assertEquals(
            response.status_code, 410, "Submit route not sending 410 GONE signal."
        )


class GenOtpTestCase(TestCase):
    """Test OTP."""

    fixtures = ["email_templates.json"]

    def test_gen_otp_form_blocking(self):
        """Test the OTP blocks failed captchas."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})

        # build a basic request to test with
        request = create_super_request({"recaptcha": "none"}, "?uuid=''")

        genotp_form = GenOtpViewSetSuper()
        response = genotp_form.create(request)


class OrderSubmitTestCase(TestCase):
    """Test Order Submit"""

    fixtures = ["email_templates.json"]
    uuid = ""

    def setUp(self):
        order = OrderFormViewSetSuper.create_order_object(
            self,
            email="TxGIO-DevOps@twdb.texas.gov",
            order={"item": 50, "email": "TxGIO-DevOps@twdb.texas.gov"},
            test_otp="12345",
        )
        order.order_approved = True
        order.approved_charge = 7.0
        order.save()
        self.uuid = str(order.id)

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
        """Test Order Submit create function"""
        submit_form_super = OrderSubmitViewSetSuper()
        request = create_super_request(
            {
                "recaptcha": "none",
                "form_id": "data-tnris-org-order",
                "accessCode": "TxGIO-DevOps@twdb.texas.gov",
                "passCode": "12345",
            },
            f"?uuid={self.uuid}",
        )
        response = submit_form_super.create(request)

        # # Make sure we get a 201 created response.
        # self.assertEquals(response.status_code, 201, "Form submission was not successful.")

        # # Make sure email is sent.
        # self.assertEqual(len(mail.outbox), 1, "No email has been sent.")


class FiservTestCase(TestCase):
    """Test Fiserv endpoints"""

    def test_make_hmac(self):
        hmac: str = api_helper.generate_fiserv_hmac()

        self.assertIsNotNone(hmac)