import requests
import os
from django.test import TestCase

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