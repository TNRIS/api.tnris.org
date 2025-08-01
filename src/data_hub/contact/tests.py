import hashlib
from django.db.models import Q
import requests
import os
import time
import json
import secrets
import datetime

from django.core import mail
from django.test import TestCase, AsyncRequestFactory
from contact.viewsets import (
    FiservGenOtpViewSet,
    FiservSubmitFormViewSet,
    FiservOrderSubmitViewSet,
    FiservOrderFormViewSet,
)
from unittest.mock import MagicMock
from contact.fdms.fiserv_payments import (
    GenOtpViewSetSuper,
    OrderFormViewSetSuper,
    OrderSubmitViewSetSuper,
    OrderStatusViewSetSuper,
    InitiateRetentionCleanupViewSetSuper,
    OrderArchivalViewSetSuper
)
from .models import OrderType, OrderDetailsType
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from contact.fdms import fiserv_helper

payload_valid_test = {
    "accountid": os.environ.get("FISERV_ACCOUNT_ID"),
    "companycode": os.environ.get("FISERV_COMPANY_CODE"),
    "currencycode": "USD",
    "customerid": os.environ.get("FISERV_CUSTOMER_ID"),
    "userid": os.environ.get("FISERV_USER_ID"),
    "templateid": 1092,
    "savepaymentmethod": "N",
    "saveatcustomer": "N",
    "displaycardssavedatcustomer": "N",
    "redirecturl": "https://example.com/checkout/confirm",
    "cancelredirecturl": "https://example.com/checkout/cancel",
    "orderid": "1234",
    "reference": "UPI",
    "purchaseorder": "1234",
    "type": "C",
    "transactionType": "S",
    "transactionamount": 11.00,
    "paymentmethod": "CC",
    "cof": "C",
    "cofscheduled": "N",
    "ecomind": "E",
    "customer": {
        "customername": "Test",
        "addressline1": "123 Main St",
        "addressline2": "",
        "city": "Houston",
        "state": "TX",
        "zipcode": "77070",
        "country": "US",
        "phone": "713-111-9999",
        "email": "test@twdb.texas.gov"
    },
    "payments": [
        {
            "mode": "CC",
            "merchantid": os.environ.get("FISERV_MERCHANT_ID")
        }
    ],
    "level3": [
        {
            "linenumber": "1.000",
            "productcode": "Orange001",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": "Orange",
            "unitcost": "3.00",
            "lineitemtotal": "3.00",
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA"
        },
        {
            "linenumber": "2.000",
            "productcode": "Green001",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": "Green",
            "unitcost": "7.00",
            "lineitemtotal": "7.00",
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA"
        },
        {
            "linenumber": "3.000",
            "productcode": "FEE",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": " fee**",
            "unitcost": "1.00",
            "lineitemtotal": "1.00",
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA"
        }
    ]
}

order_details = {
    "name": "John",
    "address": "State Parking Garage E",
    "city": "Austin",
    "state": "Texas",
    "zipcode": "76528",
    "country": "US",
    "phone": "1112223333",
    "email": str(os.environ.get("MAIL_DEFAULT_TO"))
}

PROTOCOL = "http"

FISERV_URL = str(os.environ.get("FISERV_URL"))
FISERV_URL_V2 = str(os.environ.get("FISERV_URL_V2"))
FISERV_URL_V3 = str(os.environ.get("FISERV_URL_V3"))
SEND_EMAIL = "N"
payload_valid_test = fiserv_helper.generate_fiserv_post_body("CC", "", 1092, 11.11, .50,  order_details)

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
        "name": "FIRSTNAME LASTNAME",
        "email": "TxGIO-DevOps@twdb.texas.gov",
        "phone": "1112223333",
        "address": "State Parking Garage E",
        "city": "Austin",
        "state": "Texas",
        "zipcode": "78660",
        "organization": "TEST",
        "industry": "TESTING",
        "fedex": "",
        "notes": "Test Note",
        "delivery": "Test Delivery",
        "harddrive": "Test Hard Drive",
        "payment": "CC",
        "order": "Test item 1\nTest Item 2",
        "form_id": "data-tnris-org-order",
    }

    order_details_complete= {
        "Name": "complete complete",
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

    fake_charge = {
        "accountid": os.environ.get("FISERV_ACCOUNT_ID"),  # required
        "userid": os.environ.get("FISERV_USER_ID"),  # required
        "cof": "C",  # Optional, means Card on file, and C means customer.
        "cofscheduled": "N",  # Optional, N means no don't schedule card to be filed.
        "ecomind": "E",  # Optional, E means ECommerce, this is a note on the origin of transaction
        "transactions": [{ # required
            "merchantid": os.environ.get("FISERV_MERCHANT_ID"),
            "currencycode": "USD",
            "companycode": os.environ.get("FISERV_COMPANY_CODE"),
            "customerid": os.environ.get("FISERV_CUSTOMER_ID"),
            "orderid": "", # Configured elsewhere.
            "paymentmethod": {
                "tokenid": "", # Dynamic so this is set in setuptestdata function.
                "transactionamount": "2.25",  # required
                "cvv": "123",
                "customername": "test man",
                "addressline1": "State Parking Garage E",
                "addressline2": "",
                "city": "Austin",
                "state": "Texas",
                "zip": "78701",
                "country": "US",
                "phonenumber": "1111111111",
                "email": os.environ.get("MAIL_DEFAULT_TO"),
                "type": "VISA",
                "last4": "1111",
                "routingnumber": "",
                "secureflag": "05",
                "securevalue": ""
            },
            "level3": fiserv_helper.generate_level_three("2.0", ".25"),
            "clxstream": fiserv_helper.generate_clx_stream("2.0", ".25", "", "CC"),
            "sendemailreceipts": SEND_EMAIL,
        }],
    }

    fake_charge_new = {
        "accountid": os.environ.get("FISERV_ACCOUNT_ID"),  # required
        "userid": os.environ.get("FISERV_USER_ID"),  # required
        "cof": "C",  # Optional, means Card on file, and C means customer.
        "cofscheduled": "N",  # Optional, N means no don't schedule card to be filed.
        "ecomind": "E",  # Optional, E means ECommerce, this is a note on the origin of transaction
        "transactions": [{ # required
            "merchantid": os.environ.get("FISERV_MERCHANT_ID"),
            "currencycode": "USD",
            "companycode": os.environ.get("FISERV_COMPANY_CODE"),
            "customerid": os.environ.get("FISERV_CUSTOMER_ID"),
            "orderid": "", # Configured elsewhere.
            "paymentmethod": {
                "tokenid": "", # Dynamic so this is set in setuptestdata function.
                "transactionamount": "11.01",  # required
                "cvv": "123",
                "customername": "test man",
                "addressline1": "State Parking Garage E",
                "addressline2": "",
                "city": "Austin",
                "state": "Texas",
                "zip": "78701",
                "country": "US",
                "phonenumber": "1111111111",
                "email": os.environ.get("MAIL_DEFAULT_TO"),
                "type": "VISA",
                "last4": "1111",
                "routingnumber": "",
                "secureflag": "05",
                "securevalue": ""
            },
            "level3": fiserv_helper.generate_level_three("2.0", ".25"),
            "clxstream": fiserv_helper.generate_clx_stream("2.0", ".25", "", "CC"),
            "sendemailreceipts": SEND_EMAIL,
        }],
    }

    fake_tokenize = {
        "accountid": os.environ.get("FISERV_ACCOUNT_ID"),
        "currency": "USD",
        "companycode": os.environ.get("FISERV_COMPANY_CODE"),
        "mode": "CC",
        "type": "VISA",
        "accountnumber": "4111111111111111",
        "expirationdate": "122029"
    }

    def setUp(self):
        if(self.uuid):
            # Reset otp age.
            order = OrderType.objects.get(id=self.uuid)
            order.order_details.otp_age = time.time()
            order.order_details.save()
            order.save()

    @classmethod
    def setUpTestData(cls):
        basic = fiserv_helper.generate_basic_auth()

        ofs = OrderFormViewSetSuper() # I need to call a method before creation.
        order = OrderFormViewSetSuper.create_order_object(
            MagicMock(),
            email="TxGIO-DevOps@twdb.texas.gov",
            order_details=ofs.format_req(cls.order_details_new.items()),
            test_otp="12345",
        )
        order.order_approved = True
        order.approved_charge = 7.0
        order.order_token = str(order.id)
        order.save()
        cls.uuid = str(order.id)

        submit_form_super = OrderSubmitViewSetSuper()
        request = create_super_request(
            {
                "recaptcha": "none",
                "form_id": "data-tnris-org-order",
                "accessCode": "TxGIO-DevOps@twdb.texas.gov",
                "passCode": "12345",  # Note: this is not a real passcode.
            },
            f"?uuid={cls.uuid}",
        )
        submit_form_super.create_super(request)

        fake_token_hmac = fiserv_helper.generate_fiserv_hmac(
            f"{FISERV_URL}tokenize",
            "POST",
            json.dumps(cls.fake_tokenize),
            os.environ.get("FISERV_ACCOUNT_ID"),
            os.environ.get("FISERV_AUTH_CODE"),
        )

        fake_token = requests.post(
            FISERV_URL + "tokenize",
            json=cls.fake_tokenize,
            headers={
                "accountid": os.environ.get("FISERV_ACCOUNT_ID"),  # good
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),  # good
                "signature": f"Hmac {fake_token_hmac.decode()}",
                "Authorization": f"Basic {basic.decode()}",
            },
        )
        order_id = f"580WD{os.urandom(4).hex()}" # Just for testing. 
        # configure the variables in fake_charge structure. 
        cls.fake_charge["transactions"][0]["paymentmethod"]["tokenid"] = json.loads(fake_token.text)["tokenid"]
        cls.fake_charge["transactions"][0]["orderid"] = order_id
        cls.fake_charge["transactions"][0]["clxstream"]["transaction"]["localreferenceid"] = order_id

        fake_hmac_v3 = fiserv_helper.generate_fiserv_hmac(
            f"{FISERV_URL_V3}charge",  #NOTE: Doesn't work but just testing v3
            "POST",
            json.dumps(cls.fake_charge),
            os.environ.get("FISERV_ACCOUNT_ID"),
            os.environ.get("FISERV_AUTH_CODE"),
        )

        #NOTE: Doesn't work but just testing v3
        fake_response_v3 = requests.post(  #NOTE: Doesn't work but just testing v3
            FISERV_URL_V3 + "charge",
            json=cls.fake_charge,
            headers={
                "accountid": os.environ.get("FISERV_ACCOUNT_ID"),  # good
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),  # good
                "signature": f"Hmac {fake_hmac_v3.decode()}",
                "Authorization": f"Basic {basic.decode()}",
            },
        )

        #NOTE: Doesn't work but just testing v2
        fake_hmac_v2 = api_helper.generate_fiserv_hmac(
            f"{FISERV_URL_V2}Charge",  #NOTE: Doesn't work but just testing v2
            "POST",
            json.dumps(cls.fake_charge),
            os.environ.get("FISERV_ACCOUNT_ID"),
            os.environ.get("FISERV_AUTH_CODE"),
        )

        #NOTE: Doesn't work but just testing v3
        fake_response_v3 = requests.post(  #NOTE: Doesn't work but just testing v3
            FISERV_URL_V3 + "charge",
            json=cls.fake_charge,
            headers={
                "accountid": os.environ.get("FISERV_ACCOUNT_ID"),  # good
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),  # good
                "signature": f"Hmac {fake_hmac_v3.decode()}",
                "Authorization": f"Basic {basic.decode()}",
            },
        )

        # Create fake order in the database.abs
        access_token = "TxGIO-DevOps@twdb.texas.gov"
        salt = secrets.token_urlsafe(32)
        pepper = os.environ.get("ACCESS_PEPPER")
        hash = hashlib.sha256(
            bytes(access_token + salt + pepper, "utf8")
        ).hexdigest()

        otp = secrets.token_urlsafe(12)
        order_details = OrderDetailsType.objects.create(
            details=json.dumps(cls.order_details_complete),
            access_code=hash,
            access_salt=salt,
            otp=hashlib.sha256(bytes(otp + salt + pepper, "utf8")).hexdigest(),
            otp_age=time.time(),
        )
        created = OrderType.objects.create(order_details=order_details)
        created.order_approved = True
        created.approved_charge = 23
        created.order_token = json.loads(fake_response_v3.text)["transactions"][0]["pgtransactionid"]
        created.save()

        # Put completed order in database.
        order = OrderFormViewSetSuper.create_order_object(
            MagicMock(),
            email="TxGIO-DevOps@twdb.texas.gov",
            order_details=cls.order_details_new,
            test_otp="12345",
        )
        order.order_approved = True
        order.approved_charge = 9.9
        order.order_token = "8fa45e97-439f-4883-a3fd-b42d3d7fabb1"
        order.created = datetime.datetime(2009, 1, 1, 0)
        order.last_modified = datetime.datetime(2010, 1, 1, 0)
        order.save()

        OrderType.objects.filter(order_token="8fa45e97-439f-4883-a3fd-b42d3d7fabb1").update(last_modified = datetime.datetime(2010, 1, 1, 0))

class SnappayTestCase(GeneralTest):
    """General Snappay tests"""
    fixtures = ["email_templates.json"]

    def test_order_cleanup(self):
        """Order cleanup test case."""
        order_cleanup = OrderArchivalViewSetSuper()
        request = create_super_request(
            {
                "access_code": os.environ.get("CCP_ACCESS_CODE"),
                "approve_run": "true"
            },
            f"?uuid={self.uuid}"
        )
        response = order_cleanup.create_super(request)
        self.assertEqual(response.status_code, 200, "Order Cleanup unsuccessful.")
        self.assertEqual(mail.outbox[0].subject, 'Order Received', "Dataset order update wasn't first email. ")
        self.assertEqual(len(mail.outbox), 1, 'Dataset Order Update: Payment has been received.')

    def test_initiate_retentions_cleanup(self):
        """Initiate retention cleanup test case."""
        initiate_cleanup = InitiateRetentionCleanupViewSetSuper()
        request = create_super_request(
            {"approve_run": "true", "access_code": os.environ.get("CCP_ACCESS_CODE")}
        )
        response = initiate_cleanup.create_super(request)
        self.assertEqual(response.status_code, 200, "Order status unsuccessful.")

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
        response = order_status_super.create_super(request)

        # Make sure we get a 200 created response.
        self.assertEqual(response.status_code, 200, "Order status unsuccessful.")

    def test_order_form_blocking(self):
        """Test the order form submit blocks failed captchas."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})
        order_form = FiservOrderFormViewSet()
        response = order_form.create(request)
        self.assertEqual(
            response.status_code,
            403,
            "Order submit route not sending 403 Forbidden signal.",
        )

    def test_redirect(self):
        response = requests.post(
            PROTOCOL + "://localhost:8000/v2/order/redirect?status=success",
            json=payload_valid_test
        )

    def test_order_submit_create(self):
        """Test Order Submit create function"""
        order_form_super = OrderFormViewSetSuper()
        request = create_super_request(
            {
                "recaptcha": "none",
                "form_id": "data-tnris-org-order",
                "order_details": {
                    "item": 50,
                    "PAYMENT": 5.42,
                    "EMAIL": os.environ.get("MAIL_DEFAULT_TO"),
                    "form_id": "order-received"},
                "EMAIL": os.environ.get(
                    "MAIL_DEFAULT_TO"
                ),  # Caps to test that route makes keys lowercase
                
            }
        )
        response = order_form_super.create_super(request)

        # Make sure order was submitted and created successfully.
        orders = OrderType.objects.get_queryset()
        if len(orders):  # Check there is an item
            order = orders[0]

            self.assertIsNotNone(order, "Items does not exist")

            # Make sure order details was created successfully.
            order_details = order.order_details
            self.assertIsNotNone(order_details, "Item Details does not exist")

            # Make sure we get a 201 created response.
            self.assertEqual(
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
                "order_details": {
                    "item": 50,
                    "PAYMENT": 5.43,
                    "EMAIL": os.environ.get("MAIL_DEFAULT_TO"),
                    "form_id": "order-map"
                },
                "EMAIL": os.environ.get(
                    "MAIL_DEFAULT_TO"
                ),# Caps to test that route makes keys lowercase
            }
        )
        response = order_form_super.create_super(request)

        # Make sure we get a 201 created response.
        self.assertEqual(
            response.status_code, 201, "Form submission was not successful."
        )

        # Expected two emails to be sent.
        self.assertEqual(len(mail.outbox), 2, "Wrong number of emails have been sent.")

    def test_gone(self):
        """Test that old order urls are gone."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})

        submit_form = FiservSubmitFormViewSet()
        response = submit_form.create(request)
        self.assertEqual(
            response.status_code, 410, "Submit route not sending 410 GONE signal."
        )

    def test_gen_otp_form_blocking(self):
        """Test the OTP blocks failed captchas."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})

        # build a basic request to test with
        request = create_super_request({"recaptcha": "none"}, f"?uuid={self.uuid}")

        genotp_form = FiservGenOtpViewSet()
        response = genotp_form.create(request)

        self.assertEqual(
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
        response = genotp_form.create_super(request)
        self.assertEqual(
            response.status_code,
            200,
            "Test the OTP generation failed.",
        )

        self.assertEqual(
            response.data["status"],
            "success",
            "Test the OTP generation failed.",
        )

    def test_gen_order_submit_blocking(self):
        """Test the order submit blocks failed captchas."""
        request = requests.Request(method="POST", data={"recaptcha": "none"})
        request = create_super_request({"recaptcha": "none"}, f"?uuid=bad")
        order_submit = FiservOrderSubmitViewSet()
        response = order_submit.create(request)
        self.assertEqual(
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
        response = submit_form_super.create_super(request)

        # # Make sure we get a 201 created response.
        self.assertEqual(
            response.status_code, 200, "Form submission and HPP was not created."
        )

    def test_make_hmac(self):
        requestUri: str = f"{FISERV_URL_V3}GetRequestID"
        hmac = fiserv_helper.generate_fiserv_hmac(
            requestUri,
            "POST",
            json.dumps(payload_valid_test),
            os.environ.get("FISERV_ACCOUNT_ID"),
            os.environ.get("FISERV_AUTH_CODE"),
        )
        self.assertIsNotNone(hmac)
        basic = fiserv_helper.generate_basic_auth()
        response = requests.post(
            FISERV_URL_V3 + "GetRequestID",
            json=payload_valid_test,
            headers={
                "accountid": os.environ.get("FISERV_ACCOUNT_ID"),  # good
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),  # good
                "signature": f"Hmac {hmac.decode()}",
                "Authorization": f"Basic {basic.decode()}",
            },
        )
        response_text = json.loads(response.text)
        self.assertIs(response_text["status"], "Y", "response status is not Y " + response_text["message"])
