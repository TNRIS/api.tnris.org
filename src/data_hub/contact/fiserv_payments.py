"""
    Handle the datahub and map orders using our payment provider.
"""
import hashlib
import json
import os
import re
import secrets
import time
from datetime import datetime, timezone
import requests
import traceback

from rest_framework import status, viewsets
from rest_framework.response import Response
from django.db.models.signals import pre_save
from django.dispatch import receiver
from modules.api_helper import logger
from modules import api_helper
from .models import EmailTemplate, OrderType, OrderDetailsType
from contact.fiserv_routines import fiserv_helper

CLEANING_FLAG = False
SEND_HTML_FLAG = True

FISERV_URL = os.environ.get("FISERV_URL")
FISERV_URL_V2 = os.environ.get("FISERV_URL_V2")
FISERV_URL_V3 = os.environ.get("FISERV_URL_V3")

def resend_email(self, request, queryset, CC_STRATMAP):
    cont_static = FiservViewset()

    for order in queryset:
        if order.order_approved and order.approved_charge and order.customer_notified:
            order_info = json.loads(order.order_details.details)
            formatted = cont_static.format_req(order_info.items())
            email_template = EmailTemplate.objects.get(form_id="order-approved")

            cont_static.send_template_email(
                email_template,
                {"uuid": str(order.pk)},
                formatted["email"],
                os.environ.get("STRATMAP_EMAIL"),
                SEND_HTML_FLAG,
                CC_STRATMAP
            )

# #################################################################
# Do not call these functions from django router directly.
# Call them from viewsets.py and do the authentication in viewsets.py
# This is so that we can test these functions directly.
# #################################################################
class FiservViewset(viewsets.ViewSet):
    def intro(self, request, msg=""):
        """Abstraction function to check logger, check captcha, then handle failed captchas if needed."""
        if api_helper.checkLogger():
            logger.info(msg)
        return self.create_super(request)

    def captcha_intro(self, request, msg):
        verify_req = api_helper.checkCaptcha(request.data["recaptcha"])

        # If we need to check the captcha then we verify captcha is correct.
        if json.loads(verify_req.text)["success"]:
            return self.intro(request)
        else:
            return Response(
                {"status": "failure", "message": "Captcha is incorrect."},
                status=status.HTTP_403_FORBIDDEN,
            )

    # inject form values into email template body
    def compile_email_body(self, template_body, dict):
        """
        Compile email body.
        """
        injected = template_body
        # loop form value keys and replace in template
        for k in dict.keys():
            var = "{{%s}}" % k.lower()
            injected = injected.replace(var, str(dict[k]))
        # replace all template values which weren't in the form (optional form fields)
        injected = re.sub(r"\{\{.*?\}\}", "", injected)
        return injected

    def build_error_response(self, message, e=False):
        """
        Build error message and response.
        """
        if api_helper.checkLogger() and e:
            logger.error("%s: %s", message, e)
        elif api_helper.checkLogger():
            logger.error("%s", message)
        return Response(
            {"status": "error", "message": message},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def send_template_email(self, email_template, formatted, sender, replyer, html=False, CC_EMAIL=""):
        """Send an email to the template email (Configured through API)
        sender and replyer default to mail_default to unless sendpoint
        """
        body = self.compile_email_body(email_template.email_template_body, formatted)
        if not sender:
            sender = (
                os.environ.get("MAIL_DEFAULT_TO")
                if email_template.sendpoint == "default"
                else formatted[email_template.sendpoint]
            )
        if not replyer:
            replyer = (
                formatted["email"]
                if "email" in formatted.keys()
                else "unknown@tnris.org"
            )

        # Request can support firstname or name. Check which has been passed in.
        if "name" in formatted.keys():
            replyer = f"{formatted['name']} <{formatted['email']}>"
        elif "firstname" in formatted.keys() and "lastname" in formatted.keys():
            replyer = f"{formatted['firstname']} {formatted['lastname']} <{formatted['email']}>"


        if(html == SEND_HTML_FLAG):
            api_helper.send_html_email(
                email_template.email_template_subject,
                body,
                send_to=sender,
                reply_to=replyer,
                cc_email=CC_EMAIL
            )
        else:
            # send to ticketing system unless sendpoint has alternative key value
            # in email template record
            api_helper.send_raw_email(
                email_template.email_template_subject,
                body,
                send_to=sender,
                reply_to=replyer,
                cc_email=CC_EMAIL
            )
    
    def format_req(self, items):
        return {k.lower().replace(" ", "_"): v for k, v in items}

# FiservViewset -> OrderFormViewSetSuper -> OrderFormViewSet

# FORMS ORDER ENDPOINT
class OrderFormViewSetSuper(
        FiservViewset
    ):
    """
    Handle TxGIO order form submissions through fiserv (Snap Pay).
    """
    @receiver(pre_save, sender=OrderType)
    def my_callback(sender, instance, *args, **kwargs):
        contact_viewset = FiservViewset()
        instance.order_approved
        if instance.order_approved and instance.approved_charge:
            if not instance.customer_notified:
                instance.customer_notified = True
                instance.save()
                order_info = json.loads(instance.order_details.details)
                formatted = contact_viewset.format_req(order_info.items())

                email_template = EmailTemplate.objects.get(form_id="order-approved")
                contact_viewset.send_template_email(
                    email_template,
                    {"uuid": str(instance.pk)},
                    formatted["email"],
                    os.environ.get("STRATMAP_EMAIL"),
                    SEND_HTML_FLAG
                )

            return Response(
                {"status": "success", "message": "Success"},
                status=status.HTTP_201_CREATED,
            )

    def notify_user(self, order_object, email):
        # Notify user
        email_template = EmailTemplate.objects.get(form_id="notify-user")
        self.send_template_email(
            email_template,
            {"uuid": str(order_object.id), "email": email},
            email,
            os.environ.get("STRATMAP_EMAIL"),
            SEND_HTML_FLAG
        )

    def create_order_object(self, email, order_details, test_otp=None):
        """Create the order and add it to the database."""

        try:
            access_token = email
            salt = secrets.token_urlsafe(32)
            pepper = os.environ.get("ACCESS_PEPPER")
            hash = hashlib.sha256(
                bytes(access_token + salt + pepper, "utf8")
            ).hexdigest()
            otp = secrets.token_urlsafe(12)
            if test_otp:
                otp = test_otp
            order_details = OrderDetailsType.objects.create(
                details=json.dumps(order_details),
                access_code=hash,
                access_salt=salt,
                otp=hashlib.sha256(bytes(otp + salt + pepper, "utf8")).hexdigest(),
                otp_age=time.time(),
            )
            order_details.save()
            order = OrderType.objects.create(order_details=order_details)
            order.save()

            return order
        except Exception as e:
            logger.error("Error creating order object at create_order_object.")

    def create_super(self, request):
        """Create a order object and notify"""
        try:
            # Generate Access Code and one way encrypt it.
            order_details = request.data.get("order_details")

            order_object = self.create_order_object(
                email=order_details["Email"],
                order_details=order_details
            )

            order_details["url"] = (
                request.META["HTTP_REFERER"]
                if "HTTP_REFERER" in request.META.keys()
                else request.META["HTTP_HOST"]
            )
            order_details["order_uuid"] = str(order_object.id)
            formatted_details = self.format_req(order_details.items())
            order_object.order_details.details = json.dumps(order_details)
            order_object.order_details.save()
            order_object.save()
            # gettransaction orderid must = orderid from getrequestid (getTransaction is recommended over getpaymentdetails)
            ################################################
            # Begin configuration of emails to be sent.
            ################################################
            email_template = EmailTemplate.objects.get(form_id=order_details["form_id"])
            body = self.compile_email_body(
                email_template.email_template_body, formatted_details
            )
            sender = os.environ.get("MAIL_DEFAULT_TO")
            replyer = (
                formatted_details["email"]
                if "email" in formatted_details.keys()
                else "unknown@tnris.org"
            )

            # If name was sent in request add it to the address information.
            if "name" in formatted_details.keys():
                replyer = "%s <%s>" % (formatted_details["name"], formatted_details["email"])
            # Send to ticketing system unless sendpoint has alternative key value in email template record.
            api_helper.send_raw_email(
                subject=email_template.email_template_subject,
                body=body,
                send_to=sender,
                reply_to=replyer,
            )

            # If we get this far then send a notification to the requester via email, and a 201 created response.
            self.notify_user(order_object, formatted_details["email"])
            return Response(
                {"status": "success", "message": "Success"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            if api_helper.checkLogger():
                logger.error("Error creating order")
            print(e)
            return Response(
                {"status": "failure", "message": "internal error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class GenOtpViewSetSuper(
        FiservViewset
    ):
    """
    Regenerate One Time Passcode
    """
    def create_super(self, request, format=None):
        try:
            order = OrderType.objects.get(id=request.query_params["uuid"])

            # Regenerate OTP
            otp = secrets.token_urlsafe(12)
            salt = order.order_details.access_salt
            pepper = os.environ.get("ACCESS_PEPPER")

            order.order_details.otp = hashlib.sha256(
                bytes(otp + salt + pepper, "utf8")
            ).hexdigest()
            order.order_details.otp_age = time.time()

            order.order_details.save()
            formatted_details = self.format_req(json.loads(order.order_details.details).items())

            # Send One time passcode to users email.
            # get email template for generating otp
            email_template = EmailTemplate.objects.get(form_id="gen-otp")
            formatted = self.format_req(request.data.items())
            formatted["otp"] = otp
            self.send_template_email(
                email_template,
                formatted,
                formatted_details["email"],
                os.environ.get("STRATMAP_EMAIL"),
                SEND_HTML_FLAG
            )

            if api_helper.checkLogger():
                logger.info("Passcode sent to email.")
            return Response(
                {"status": "success", "message": "Passcode sent to email."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            message = "Error generating the One time passcode. Exception: "
            if api_helper.checkLogger():
                message = message + str(e)
                logger.error(message)
            return Response(
                {"status": "failure", "message": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class OrderStatusViewSetSuper(
        FiservViewset
    ):
    """
    Handle Checking the order status
    """
    def create_super(self, request, format=None):
        order = OrderType.objects.get(id=request.query_params["uuid"])
        authorized = api_helper.auth_order(request.data, order)
        if not authorized:
            return Response(
                {
                    "status": "denied",
                    "message": "Access is denied. Either access code is wrong or One time passcode has expired.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        elif order and order.archived:
            return Response(
                {
                    "status": "failure",
                    "message": "Order not found. Or order has been processed.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        elif order and order.order_approved:
            return Response(
                {"status": "success", "message": "Pending Payment."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "success", "message": "Pending Review."},
                status=status.HTTP_200_OK,
            )

class InitiateRetentionCleanupViewSetSuper(
        FiservViewset
    ):
    """
    Delete old orders according to retention policy.
    """

    def create_super(self, request, format=None):
        """Delete old orders according to retention policy."""

        # Check CCP ACCESS CODE to prevent bots from making requests.
        if os.environ.get("CCP_ACCESS_CODE") != request.data["access_code"]:
            if api_helper.checkLogger():
                logger.error("CCP access code incorrect in InitiateRetentionCleanup ")
            return Response(
                {"status": "access_denied", "message": "access_denied"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Boolean flag to determine if we are running a test or not.
        approve_run = False
        if "approve_run" in request.data:
            approve_run = request.data["approve_run"] == "true"

        try:
            orders = OrderType.objects.get_queryset()
            # Loop over each order and check if the retention policy has expired them.
            for order in orders:
                # Determine how long since the order was created.
                created_td = datetime.utcnow() - order.created.replace(tzinfo=None)
                days_since_created = created_td.days

                # Determine how long since the order was modified.
                modified_td = datetime.utcnow() - order.last_modified.replace(
                    tzinfo=None
                )
                days_since_modified = modified_td.days

                # Get associated order details.
                order_details = OrderDetailsType.objects.filter(
                    id=order.order_details_id
                )

                # If archived we must check if deletion time has come.
                # This is where the writing to the database should occur. Be
                # sure to check for "approve_run" is "true" before doing
                # anything dangerous.
                if order.archived is True:
                    # Retention policy - Un-acted upon orders will be archived
                    # after 90 days. After an additional 30 days then they will
                    # be deleted from the API database. We can check that at
                    # least 120 days have passed since that's the minimum
                    # amount of time we want to keep an order. We also want to
                    # make sure it was changed to archived and it hasn't been
                    # modified in any way for 30 days.
                    if (days_since_created > 120) and (days_since_modified > 30):
                        if approve_run:
                            order.delete()
                            order_details.delete()
                else:
                    # If not archived we check the retention policy.
                    # Retention policy Orders marked as archived will be
                    # deleted if left in that state for 30 days completely
                    # unmodified.
                    if (days_since_created > 90) and (days_since_modified > 90):
                        if approve_run:
                            order.archived = True
                            order.save()

            # General Response
            if approve_run:
                return Response({"status": "success", "message": "success"})

        except Exception as e:
            if api_helper.checkLogger():
                logger.info("Error cleaning up old orders: %s", str(e))
            return Response(
                {"status": "failure", "message": "The order has failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class OrderCleanupViewSetSuper(FiservViewset):
    """
    Begin Cleanup routines
    """
    def create_super(self, request, format=None):
        global CLEANING_FLAG
        if CLEANING_FLAG:
            if api_helper.checkLogger():
                logger.error("Cleaning function is already in progress.")
            return Response(
                {
                    "status": "failure",
                    "message": "failure. Cleaning function already running",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Check CCP ACCESS CODE to prevent bots from making requests.
        if os.environ.get("CCP_ACCESS_CODE") != request.data["access_code"]:
            if api_helper.checkLogger():
                logger.error("CCP access code incorrect")
            return Response(
                {"status": "access_denied", "message": "access_denied"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            # Select all of the orders that are not archived.
            if api_helper.checkLogger():
                logger.info("Starting cleanup.")
            CLEANING_FLAG = True
            unarchived_orders = OrderType.objects.filter(archived=False).values()

            now = datetime.now(timezone.utc)

            # If an order is older than 15 days archive it regardless.
            for order in unarchived_orders:
                try:
                    difference = now - order["created"]
                    request.query_params._mutable = True
                    request.query_params["uuid"] = str(order["id"])
                    request.query_params._mutable = False
                    receipt = self.get_receipt(request, format)
                    if receipt.status_code == 200: 
                        if not order["tnris_notified"]:
                            if api_helper.checkLogger():
                                logger.info(
                                    "Order receipt found where TxGIO has not been notified."
                                )
                            obj = OrderType.objects.get(id=order["id"])
                            obj.tnris_notified = True
                            order_obj = json.loads(
                                OrderDetailsType.objects.filter(
                                    id=order["order_details_id"]
                                ).values()[0]["details"]
                            )
                            obj.save()

                            order_string = api_helper.buildOrderString(order_obj)

                            reply_email = "unknown@tnris.org"
                            if "Email" in order_obj:
                                reply_email = order_obj["Email"]

                            email_template = EmailTemplate.objects.get(form_id="order-received")
                            self.send_template_email(
                                email_template,
                                {"order_id": order["id"], "order_string": order_string},
                                os.environ.get("MAIL_DEFAULT_TO"),
                                reply_email,
                            )

                    # If no receipt was received or order was sent after 90 days then archive order automatically.
                    if difference.days > 90 and (
                        receipt.status_code != 200 or order["order_sent"] == True
                    ):
                        order_obj = json.loads(
                            OrderDetailsType.objects.filter(
                                id=order["order_details_id"]
                            ).values()[0]["details"]
                        )
                        obj = OrderType.objects.get(id=order["id"])
                        obj.archived = True
                        obj.save()

                        if receipt.status_code != 200 and "Email" in order_obj:
                            email_template = EmailTemplate.objects.get(form_id="order-removed")
                            self.send_template_email(
                                email_template,
                                {},
                                order_obj["Email"],
                                os.environ.get("STRATMAP_EMAIL"),
                            )
                except Exception as e:
                    if api_helper.checkLogger():
                        logger.error(
                            "There was a problem processing a single order. Proceeding."
                        )
            if api_helper.checkLogger():
                logger.info("Successful cleanup")
            response = Response(
                {"status": "success", "message": "success"},
                status=status.HTTP_200_OK,
            )
            # return response
        except Exception as e:
            message = "Error cleaning up orders. Exception: "  + str(e)
            if api_helper.checkLogger():
                logger.error(message)
            response = Response(
                {"status": "failure", "message": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            if api_helper.checkLogger():
                logger.info("Finished cleanup.")
            CLEANING_FLAG = False
            return response

    def get_receipt(self, request, format):
        # Look for a successful receipt. Otherwise return 404.
        try:
            order = OrderType.objects.get(id=request.query_params["uuid"])
            if order.order_approved:
                endpoint = f"{FISERV_URL}GetPaymentDetails" # Change over to gettransaction
                basic = fiserv_helper.generate_basic_auth()

                body = { # check orderid here.
                    "accountid": os.environ.get("FISERV_DEV_ACCOUNT_ID"),
                    "token": str(order.order_token)
                }

                hmac = fiserv_helper.generate_fiserv_hmac(
                    endpoint,
                    "POST",
                    json.dumps(body),
                    os.environ.get("FISERV_DEV_ACCOUNT_ID"),
                    os.environ.get("FISERV_DEV_AUTH_CODE"),
                )

                headers = {
                    "Accountid": os.environ.get("FISERV_DEV_ACCOUNT_ID"),  # good
                    "Signature": f"Hmac {hmac.decode()}",
                    "Authorization": f"Basic {basic.decode()}",
                    "Content-Type": "application/json"
                }

                orderinfo = requests.post(
                    endpoint,
                    json=body,
                    headers=headers,
                )

                orderContent = json.loads(orderinfo.content)
                if orderContent['status'] == "Y":
                    orders = orderContent["transaction"]
                    response = Response(
                        {
                            "status_code": orderinfo.status_code,
                            "orderReceipt": orders,
                        }
                    )
                else:
                    response = Response(
                        {"status_code": 404}, status=status.HTTP_404_NOT_FOUND
                    )
            else:
                response = Response(
                    {"status_code": 404}, status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            response = Response(
                {"status_code": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            message = "Error getting receipt: "  + str(e)
            if api_helper.checkLogger():
                logger.error(message)
        finally:
            return response

class OrderSubmitViewSetSuper(
        FiservViewset
    ):
    """
    Create and return a fiserv order url to HPP.
    """

    def create_super(self, request, format=None):
        try:
            orderObj = OrderType.objects 
            order = orderObj.get(id=request.query_params["uuid"])
            authorized = api_helper.auth_order(request.data, order)
            if not authorized:
                return Response(
                    {
                        "status": "denied",
                        "order_url": "NONE",
                        "message": "Access is denied. Either access code is wrong or One time passcode has expired.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            order_details = json.loads(order.order_details.details)
            order_details = self.format_req(order_details.items())

            total = round(order.approved_charge, 2)
            # 2.25% and $.25
            transactionfee = round(((total + 0.25) / 100) * 2.25, 2)
            # Round to second digit because of binary Float
            transactionfee = round(transactionfee + 0.25, 2)
            template_id = 1092 #Configure the default
            payment_method = "CC"
            if "payment" in order_details:
                # In this case read in the payment method from the body.
                payment_method = order_details["payment"]
                if payment_method == "ACH":
                    template_id = 1093
                elif payment_method == "CC":
                    template_id = 1092
            elif "payment_method" in order_details:
                if order_details["payment_method"] == "Credit Card":
                    payment_method = "CC"
                    template_id = 1092
                else:
                    payment_method = order_details["payment_method"]
                    template_id = 1093

            body = fiserv_helper.generate_fiserv_post_body(payment_method, str(order.order_details_id), template_id, total, transactionfee, order_details)
            requestUri = f"{FISERV_URL_V3}GetRequestID"
            hmac = fiserv_helper.generate_fiserv_hmac(
                requestUri,
                "POST",
                json.dumps(body),
                os.environ.get("FISERV_DEV_ACCOUNT_ID"),
                os.environ.get("FISERV_DEV_AUTH_CODE"),
            )
            basic = fiserv_helper.generate_basic_auth()
            response = requests.post(
                requestUri,
                json=body,
                headers={
                    "accountid": os.environ.get("FISERV_DEV_ACCOUNT_ID"),  # good
                    "merchantid": os.environ.get("FISERV_MERCHANT_ID"),  # good
                    "signature": f"Hmac {hmac.decode()}",
                    "Authorization": f"Basic {basic.decode()}",
                },
            )

            rbody = json.loads(response.text)
            hpp_page = str(os.environ.get("FISERV_HPP_PAGE"))
            if "requestid" in rbody and len(rbody['requestid']) > 0:
                orderObj.filter(id=request.query_params["uuid"]).update(
                    order_token=rbody["requestid"],
                    order_url=f"{hpp_page}ProcessRequest?reqNo={rbody['requestid']}",
                )
                order = orderObj.get(id=request.query_params["uuid"])

                response = Response(
                    {
                        "status": "success",
                        "order_url": order.order_url,
                        "charge": order.approved_charge,
                        "message": "success",
                    }
                )
            else:
                if api_helper.checkLogger():
                    logger.error(
                        f"An order has failed to be created, because there was no requestid or order has already been completed."
                    )
                response = Response(
                    {
                        "status": "failure",
                        "order_url": "NONE",
                        "message": "We could not process this order, because we couldn't find the request id or the order has already been completed.",
                    },
                    status=status.HTTP_409_CONFLICT,
                )
        except Exception as e:
            if api_helper.checkLogger():
                print(traceback.format_exc()) 
                logger.error(f"Error creating order. Exception: {str(e)}")
            response = Response(
                {
                    "status": "failure",
                    "order_url": "NONE",
                    "message": "The order has failed",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return response