import requests
import os
from django import http
from django.test import TestCase
from contact.viewsets import SubmitFormViewSet

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
            self.assertIsNotNone(res['orders_to_be_archived'])

        if 'orders_to_be_deleted' in res:
            self.assertIsNotNone(res['orders_to_be_deleted'])

class SubmitFormTestCase(TestCase):
    """Test for the Payment portal."""
    def test_submit_form(self):
        """Test the payment portal."""

        request = http.HTTPRequest()
        

        payload = """{
            pw: obj["data-email"],
            order_details: {
                Name: `${obj["data-first-name"]} ${obj["data-last-name"]}`,
                Email: obj["data-email"],
                Phone: obj["data-phone"],
                Address: obj["data-address"],
                City: obj["data-city"],
                State: obj["data-state"],
                Zipcode: obj["data-zipcode"],
                Organization: obj["data-organization"],
                Industry: obj["data-industry"],
                Fedex: obj["data-fedex"],
                Notes: obj["data-notes"],
                Delivery: obj["data-delivery-method"],
                HardDrive: obj["data-hard-drive"],
                Payment: obj["data-payment-method"],
                Order: cartOrderText.join("\n"),
                form_id: "data-tnris-org-order"
            },
            recaptcha: obj["g-recaptcha-response"]
        }"""