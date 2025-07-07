from rest_framework.permissions import AllowAny
from rest_framework import status, viewsets
from rest_framework.response import Response
from datetime import datetime, timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save
from django.dispatch import receiver
from modules import api_helper_v1
from .models import EmailTemplate, OrderType, OrderDetailsType
from .serializers import *

import requests, os, json, re, sys, hashlib, secrets, time
import logging, watchtower

logger = logging.getLogger("errLog")
logger.addHandler(watchtower.CloudWatchLogHandler())
CLEANING_FLAG=False

# Use testing URLS (Do not use in production)
TESTING = True

CCP_URL = 'https://securecheckout.cdc.nicusa.com/ccprest/api/v1/TX/'

if(TESTING):
    CCP_URL = 'https://securecheckout-uat.cdc.nicusa.com/ccprest/api/v1/TX/'

class CorsPostPermission(AllowAny):
    """
    custom permissions for cors control
    """
    whitelisted_domains = [
        "api.tnris.org",
        "beta.tnris.org",
        "data.tnris.org",
        "alphabetadata.tnris.org",
        "api-test.tnris.org",
        "betadata.tnris.org",
        "develop.tnris.org",
        "lake-gallery.tnris.org",
        "localhost:8000",
        "localhost",
        "staging.tnris.org",
        "stagingapi.tnris.org",
        "staginghub.tnris.org",
        "store.tnris.org",
        "tnris.org",
        "www.tnris.org",
        "dev.txgio.org",
        "geographic.texas.gov",
        "dev.geographic.texas.gov",
        "staging.geographic.texas.gov",
        "dev.gio.texas.gov",
        "staging.gio.texas.gov",
        "data.geographic.texas.gov",
        "data.gio.texas.gov",
        "devdata.geographic.texas.gov",
        "stagingdata.geographic.texas.gov",
        "cmsdev",
        "cmsprod"
    ]

    def has_permission(self, request, view):
        u = (
            urlparse(request.META["HTTP_REFERER"]).hostname
            if "HTTP_REFERER" in request.META.keys()
            else request.META["HTTP_HOST"]
        )
        return u in self.whitelisted_domains

class CcpViewSet(viewsets.ViewSet):
    """
    Generic CCP Class.
    """
    def intro(self, request, msg=""):
        """Abstraction function to check logger, check captcha, then handle failed captchas if needed."""
        if api_helper_v1.checkLogger():
            logger.info(msg)
        return self.create_super(request)

    def captcha_intro(self, request, msg):
        verify_req = api_helper_v1.checkCaptcha(request.data["recaptcha"])

        # If we need to check the captcha then we verify captcha is correct.
        if json.loads(verify_req.text)["success"]:
            return self.intro(request)
        else:
            return Response(
                {"status": "failure", "message": "Captcha is incorrect."},
                status=status.HTTP_403_FORBIDDEN,
            )

class SubmitFormViewSetSuper(CcpViewSet):
    """
    Handle TxGIO form submissions (Restricted Access)
    """
    # inject form values into email template body
    def compile_email_body(self, template_body, dict):
        injected = template_body
        # loop form value keys and replace in template
        for k in dict.keys():
            var = "{{%s}}" % k
            injected = injected.replace(var, str(dict[k]))
        # replace all template values which weren't in the form (optional form fields)
        injected = re.sub(r"\{\{.*?\}\}", "", injected)
        return injected

    # generic function for sending email associated with form submission
    # emails send to supportsystem to create tickets in the ticketing system
    # which are ultimately managed by IS, RDC, and StratMap
    def send_email(
        self,
        subject,
        body,
        send_from=os.environ.get("MAIL_DEFAULT_FROM"),
        send_to=os.environ.get("MAIL_DEFAULT_TO"),
        reply_to="unknown@tnris.org",
    ):
        email = EmailMessage(subject, body, send_from, [send_to], reply_to=[reply_to])
        email.send(fail_silently=False)
        return

    def create_super(self, request, format=None):
        # get email template for form. if bad form, return error
        try:
            email_template = EmailTemplate.objects.get(form_id=request.data["form_id"])
        except:
            if(api_helper_v1.checkLogger()):
                logger.error("form_id not registered.")
            return Response(
                {"status": "error", "message": "form_id not registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        formatted = {
            k.lower().replace(" ", "_"): v for k, v in request.data.items()
        }
        formatted["url"] = (
            request.META["HTTP_REFERER"]
            if "HTTP_REFERER" in request.META.keys()
            else request.META["HTTP_HOST"]
        )
        serializer = getattr(
            sys.modules[__name__], email_template.serializer_classname
        )(data=formatted)
        if serializer.is_valid():
            serializer.save()
            body = self.compile_email_body(
                email_template.email_template_body, formatted
            )
            # send to ticketing system unless sendpoint has alternative key value in email template record
            sender = (
                os.environ.get("MAIL_DEFAULT_TO")
                if email_template.sendpoint == "default"
                else formatted[email_template.sendpoint]
            )
            replyer = (
                formatted["email"]
                if "email" in formatted.keys()
                else "unknown@tnris.org"
            )
            if "name" in formatted.keys():
                replyer = "%s <%s>" % (formatted["name"], formatted["email"])
            elif "firstname" in formatted.keys() and "lastname" in formatted.keys():
                replyer = "%s %s <%s>" % (
                    formatted["firstname"],
                    formatted["lastname"],
                    formatted["email"],
                )
            self.send_email(
                email_template.email_template_subject,
                body,
                send_to=sender,
                reply_to=replyer,
            )
            if(api_helper_v1.checkLogger()):
                logger.info("Form Submitted Successfully!")
            return Response(
                {"status": "success", "message": "Form Submitted Successfully!"},
                status=status.HTTP_201_CREATED,
            )
        if(api_helper_v1.checkLogger()):
            logger.info("Serializer Save Failed.")
        return Response(
            {
                "status": "error",
                "message": "Serializer Save Failed.",
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class GenOtpViewSetSuper(CcpViewSet):
    """
    Regenerate One Time Passcode
    """
    def create_super(self, request, format=None):
        try:
            order = OrderType.objects.get(id=request.query_params["uuid"])
            details = json.loads(order.order_details.details)
            
            # Regenerate OTP
            otp = secrets.token_urlsafe(12)
            salt = order.order_details.access_salt
            pepper = os.environ.get("ACCESS_PEPPER")

            order.order_details.otp = hashlib.sha256(bytes(otp + salt + pepper, 'utf8')).hexdigest()
            order.order_details.otp_age=time.time()
            
            order.order_details.save()
            
            # Send One time passcode to users email.
            api_helper_v1.send_email(
                subject="DataHub one time passcode",
                body=
                    """
                        <html><body style='overflow:hidden'>
                    """
                    + "<div style='width: 98%; background-color: #1e8dc1;'>" +
                    """
                        <img class="TnrisLogo" width="100" height="59" src="https://cdn.tnris.org/images/txgio_light.png" alt="TxGIO Logo" title="data.geographic.texas.gov">
                        </div><br /><br />
                        Greetings from TxGIO,<br /><br />
                        Your one time passcode is: <strong>%s</strong><br /><br />
                        Thanks,<br />
                        The TxGIO Team
                    </body></html>
                    """ % otp,
                send_to=details["Email"],
                reply_to=os.environ.get("STRATMAP_EMAIL")
            )
            if(api_helper_v1.checkLogger()):
                logger.info("Passcode sent to email.")
            return Response(
                {"status": "success", "message": "Passcode sent to email."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            message = "Error generating the One time passcode. Exception: "
            if(api_helper_v1.checkLogger()): 
                message = message + str(e)
                logger.error(message)
            return Response(
                {"status": "failure", "message": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )  
    
class OrderStatusViewSetSuper(CcpViewSet):
    """
    Handle Checking the order status
    """
    def create_super(self, request, format=None):
        try:
            order = OrderType.objects.get(id=request.query_params["uuid"])
            authorized = api_helper_v1.auth_order(request.data, order)
            if(not authorized):
                return Response({"status": "denied", "message": "Access is denied. Either access code is wrong or One time passcode has expired."},
                status=status.HTTP_403_FORBIDDEN,
            )
            elif(order and order.archived):
                return Response(
                    {"status": "failure", "message": "Order not found. Or order has been processed."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            elif(order and order.order_approved):   
                return Response(
                    {"status": "success", "message": "Pending Payment."},
                    status=status.HTTP_200_OK,
                )
            else: 
                return Response(
                    {"status": "success", "message": "Pending Review."},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            message = "Error checking order status. Exception: "
            if(api_helper_v1.checkLogger()): 
                message = message + str(e)
                logger.error(message)
            return Response(
                {"status": "failure", "message": "Order not found. Or order has been processed."},
                status=status.HTTP_404_NOT_FOUND,
            )

class InitiateRetentionCleanupViewSetSuper(CcpViewSet):
    """
    Delete old orders according to retention policy.
    """
    def create_super(self, request, format=None):
        """Delete old orders according to retention policy."""

        # Check CCP ACCESS CODE to prevent bots from making requests.
        if os.environ.get("CCP_ACCESS_CODE")!= request.data["access_code"]:
            if api_helper_v1.checkLogger():
                logger.error("CCP access code incorrect in InitiateRetentionCleanup ")
            return Response(
                {"status": "access_denied", "message": "access_denied"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Boolean flag to determine if we are running a test or not.
        approve_run = False
        if 'approve_run' in request.data:
            approve_run = request.data["approve_run"] == "true"

        try:
            orders = OrderType.objects.get_queryset()
            # Loop over each order and check if the retention policy has expired them.
            for order in orders:
                # Determine how long since the order was created.
                created_td = datetime.utcnow() - order.created.replace(tzinfo=None)
                days_since_created = created_td.days

                # Determine how long since the order was modified.
                modified_td = datetime.utcnow() - order.last_modified.replace(tzinfo=None)
                days_since_modified = modified_td.days

                # Get associated order details.
                order_details = OrderDetailsType.objects.filter(id=order.order_details_id)

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
            
            # Testing information response.
            return Response({
                "status": "success",
                "message": "success"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            if api_helper_v1.checkLogger():
                logger.info("Error cleaning up old orders: %s", str(e))
            return Response({
                "status": "failure",
                "message": "The order has failed"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderCleanupViewSetSuper(CcpViewSet):
    def create_super(self, request, format=None):
        global CLEANING_FLAG
        response = None #Placeholder to verify in finally block.

        if CLEANING_FLAG:
            if api_helper_v1.checkLogger():
                logger.error("Cleaning function is already in progress.")
            return Response(
                {"status": "failure", "message": "failure. Cleaning function already running"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
        # Check CCP ACCESS CODE to prevent bots from making requests.
        if(os.environ.get("CCP_ACCESS_CODE")!= request.data["access_code"]):
            if api_helper_v1.checkLogger():
                logger.error("CCP access code incorrect")
            return Response(
                {"status": "access_denied", "message": "access_denied"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            # Select all of the orders that are not archived.
            if api_helper_v1.checkLogger():
                logger.info("Starting cleanup.")
            CLEANING_FLAG=True
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
                    if(receipt.status_code == 200):
                        if(not order["tnris_notified"]):
                            if api_helper_v1.checkLogger():
                                logger.info("Order receipt found where TxGIO has not been notified.")
                            obj = OrderType.objects.get(id=order["id"])
                            obj.tnris_notified = True
                            order_obj = json.loads(OrderDetailsType.objects.filter(id=order["order_details_id"]).values()[0]["details"])
                            obj.save()


                            order_string = api_helper_v1.buildOrderString(order_obj)
                            email_body = """
A payment has been received from from: https://data.geographic.texas.gov/order/
Please see order details below. And ship the order. \n
Form ID: data-tnris-org-order
Order ID: %s
Form parameters
================== \n
""" % str(order["id"])
                            
                            email_body = email_body + order_string
                            reply_email = "unknown@tnris.org"
                            if("Email" in order_obj):
                                reply_email = order_obj["Email"]
                            api_helper_v1.send_raw_email(subject="Dataset Order Update: Payment has been received.", body=email_body,
                                send_from=os.environ.get("MAIL_DEFAULT_FROM"),
                                send_to=os.environ.get("MAIL_DEFAULT_TO"),
                                reply_to=reply_email)
                        
                    #If no receipt was received or order was sent after 90 days then archive order automatically.
                    if(difference.days > 90 and (receipt.status_code != 200 or order["order_sent"] == True) ):
                        order_obj = json.loads(OrderDetailsType.objects.filter(id=order["order_details_id"]).values()[0]["details"])
                        obj = OrderType.objects.get(id=order["id"])
                        obj.archived = True
                        obj.save()
                        if(receipt.status_code != 200 and "Email" in order_obj):
                            api_helper_v1.send_email(
                                subject="Your TxGIO Datahub order has been removed",
                                body=
                                    """
                                        <html><body style='overflow:hidden'>
                                    """
                                    + "<div style='width: 98%; background-color: #1e8dc1;'>" +
                                    """
                                        <img class="TnrisLogo" width="100" height="59" src="https://cdn.tnris.org/images/txgio_light.png" alt="TxGIO Logo" title="data.tnris.org">
                                    </div><br /><br />
                                        Greetings from TxGIO,<br /><br />
                                        Your TxGIO Datahub order has been closed due to being greater than 90 days old. <br />
                                        For questions or concerns, Please reply to this email or visit our <a href='https://tnris.org/contact/'>contact page</a> for more ways to contact TxGIO.<br /><br />
                                        Thanks,<br />
                                        The TxGIO Team
                                        </body></html>
                                    """,
                                send_to=order_obj["Email"],
                                reply_to=os.environ.get("STRATMAP_EMAIL")
                            )
                except Exception as e:
                    if api_helper_v1.checkLogger():
                        logger.error("There was a problem processing a single order. Proceeding.")
            if api_helper_v1.checkLogger():
                logger.info("Successful cleanup")
            response =  Response(
                {"status": "success", "message": "success"},
                status=status.HTTP_200_OK,
            )
            # return response
        except Exception as e:
            message = "Error cleaning up orders. Exception: "
            if(settings.DEBUG): message = message + str(e)
            if api_helper_v1.checkLogger():
                logger.error(message + str(e))
            response =  Response(
                {"status": "failure", "message": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            if api_helper_v1.checkLogger():
                logger.info("Finished cleanup.")
            CLEANING_FLAG=False

            if(not response):
                response = Response({"status": "failure", "message": "response failure."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
    
    def get_receipt(self, request, format):
        #Look for a successful receipt. Otherwise return 404.
        try:
            order = OrderType.objects.get(id=request.query_params["uuid"])
            if(order.order_approved):
                headers = {
                    "apiKey": os.environ.get("CCP_API_KEY"),
                    "MerchantKey": os.environ.get("CCP_MERCHANT_KEY"),
                    "MerchantCode": os.environ.get("CCP_MERCHANT_CODE"),
                    "ServiceCode": os.environ.get("CCP_SERVICE_CODE")
                }
                if(TESTING):
                    headers["apiKey"] = os.environ.get("CCP_API_KEY_UAT")
                
                orderinfo = requests.get(CCP_URL + "tokens/" + str(order.order_token), headers=headers) 
                
                orderContent = json.loads(orderinfo.content)
                if('orders' in orderContent):
                    orders = orderContent["orders"]
                    if(orders[0]["orderStatus"] == "COMPLETE"):
                        orderReceipt = requests.get(CCP_URL + "receipts/" + str(orders[0]['orderId']), headers=headers)
                        response = Response(
                            {"status_code": orderReceipt.status_code, "orderReceipt": orderReceipt}
                        )
                    else:
                        response = Response(
                            {"status_code": 404},
                            status=status.HTTP_404_NOT_FOUND
                        )
                else:
                    response = Response(
                        {"status_code": 404},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                response = Response(
                    {"status_code": 404},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            response = Response(
                {"status_code": 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            message = "Error getting receipt: " 
            if(settings.DEBUG):
                message = message + str(e)
                if api_helper_v1.checkLogger():
                    logger.error(message)
        finally:
            return response

class OrderSubmitViewSetSuper(CcpViewSet):
    permission_classes = [CorsPostPermission]
    def create_super(self, request, format=None):
        try:
            if api_helper_v1.checkLogger():
                logger.info("Starting OrderSubmitViewSet")
            verify_req = api_helper_v1.checkCaptcha(request.data["recaptcha"])
            if json.loads(verify_req.text)["success"]:
                orderObj = OrderType.objects
                order = orderObj.get(id=request.query_params["uuid"])
                authorized = api_helper_v1.auth_order(request.data, order)
                if(not authorized):
                    return Response({"status": "denied",
                                    "order_url": "NONE",
                                    "message": "Access is denied. Either access code is wrong or One time passcode has expired."},
                    status=status.HTTP_403_FORBIDDEN,
                )
                order_details = json.loads(order.order_details.details)

                item_attributes = [
                                    {
                                    "FieldName": "USASLINES",
                                    "FieldValue": 3
                                    },
                                    {
                                    "FieldName": "USAS1CO",
                                    "FieldValue": 3719
                                    },
                                    {
                                    "FieldName": "USAS1PCA",
                                    "FieldValue": 19001
                                    },
                                    {
                                    "FieldName": "USAS1TCODE",
                                    "FieldValue": 195
                                    },
                                    {
                                    "FieldName": "USAS2CO",
                                    "FieldValue": 3879
                                    },
                                    {
                                    "FieldName": "USAS2PCA",
                                    "FieldValue": "07768"
                                    },
                                    {
                                    "FieldName": "USAS2TCODE",
                                    "FieldValue": 179
                                    },
                                    {
                                    "FieldName": "USAS3CO",
                                    "FieldValue": 7219
                                    },
                                    {
                                    "FieldName": "USAS3TCODE",
                                    "FieldValue": 265
                                    },
                                    {
                                    "FieldName": "USAS3PCA",
                                    "FieldValue": "07768"
                                    }
                                ]
                
                total = round(order.approved_charge, 2)
                #2.25% and $.25
                transactionfee = round(((total + .25)/100) * 2.25, 2)
                #Round to second digit because of binary Float
                transactionfee = round(transactionfee + .25, 2)

                payment = "CC" #Default to CC Payment type unless payment is specified
                if "Payment" in order_details:
                    payment = order_details["Payment"]
                elif "Payment Method" in order_details:
                    if(order_details["Payment Method"] == "Credit Card"):
                        payment = "CC"

                body = {
                    "OrderTotal": round(total + transactionfee, 2),
                    "MerchantCode": os.environ.get("CCP_MERCHANT_CODE"),
                    "MerchantKey": os.environ.get("CCP_MERCHANT_KEY"),
                    "ServiceCode": os.environ.get("CCP_SERVICE_CODE"),
                    "UniqueTransId": order.order_details_id,
                    "LocalRef": "580WD" + str(order.order_details_id),
                    "PaymentType": payment,
                    "SuccessUrl":"https://data.geographic.texas.gov/order/redirect?status=success",
                    "FailureUrl":"https://data.geographic.texas.gov/order/redirect?status=failure",
                    "CancelUrl":"https://data.geographic.texas.gov/order/redirect?status=cancel",
                    "DuplicateUrl":"https://data.geographic.texas.gov/order/redirect?status=duplicate",
                    "BCCEmail1":os.environ.get("BCC_EMAIL_1"),
                    "LineItems": [
                        {
                            "Sku": "DHUB",
                            "Description": "TxGIO DataHub order",
                            "UnitPrice": round(total + transactionfee, 2),
                            "Quantity": 1,
                            "ItemAttributes": item_attributes
                        }
                    ]
                }
                
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'USAS1AMOUNT', 'FieldValue': total})
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'USAS2AMOUNT', 'FieldValue': transactionfee})
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'USAS3AMOUNT', 'FieldValue': transactionfee})
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'CONV_FEE', 'FieldValue': transactionfee})
                api_key = os.environ.get("CCP_API_KEY")

                if(TESTING):
                    api_key = os.environ.get("CCP_API_KEY_UAT")

                x = requests.post(
                    CCP_URL + "tokens", 
                    json = body,
                    headers={
                        "apiKey": api_key
                    }
                )

                url = json.loads(x.text)
                if('htmL5RedirectUrl' in url):
                    orderObj.filter(id=request.query_params["uuid"]).update(order_token=url["token"], order_url=url["htmL5RedirectUrl"])
                    order = orderObj.get(id=request.query_params["uuid"])

                    #response = redirect(order.order_url)
                    response = Response(
                        {"status": "success", 
                        "order_url": order.order_url,
                        "charge": order.approved_charge,
                        "message": "success"}
                    )
                else:
                    if api_helper_v1.checkLogger():
                        logger.error("An order has failed. because no html5Redirect found in the response.")
                    response =  Response(
                        {"status": "failure", "order_url": "NONE", "message": "The order has failed"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
            else:
                if api_helper_v1.checkLogger():
                    logger.info("An order has failed because Captcha is incorrect.")
                return Response(
                    {"status": "failure", "message": "Captcha is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )         
        except Exception as e:
            message = "Error creating order. Exception: "
            if(settings.DEBUG):
                message = message + str(e)
                if api_helper_v1.checkLogger():
                    logger.error(message)
            response =  Response(
                {"status": "failure", "order_url": "NONE", "message": "The order has failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        return response

# FORMS ORDER ENDPOINT
class OrderFormViewSetSuper(CcpViewSet):
    """
    Handle TxGIO order form submissions
    """
    permission_classes = [CorsPostPermission]

    # inject form values into email template body
    def compile_email_body(self, template_body, dict):
        injected = template_body
        # loop form value keys and replace in template
        for k in dict.keys():
            var = "{{%s}}" % k.lower()
            injected = injected.replace(var, str(dict[k]))
        # replace all template values which weren't in the form (optional form fields)
        injected = re.sub(r"\{\{.*?\}\}", "", injected)
        return injected

    @receiver(pre_save, sender=OrderType)
    def my_callback(sender, instance, *args, **kwargs):
        instance.order_approved
        if(instance.order_approved and instance.approved_charge):
            if(not instance.customer_notified):
                instance.customer_notified = True
                instance.save()
                order_info = json.loads(instance.order_details.details)
                api_helper_v1.send_email(
                    subject="Your TxGIO Datahub order has been approved",
                    body=
                        """
                            <html><body style='overflow:hidden'>
                        """
                        + "<div style='width: 98%; background-color: #1e8dc1;'>" +
                        """
                            <img class="TnrisLogo" width="100" height="59" src="https://cdn.tnris.org/images/txgio_light.png" alt="TxGIO Logo" title="data.geographic.texas.gov">
                            </div><br /><br />
                            Greetings from TxGIO,<br /><br />
                            Your TxGIO Datahub order has been approved.<br />
                            To make a payment please follow this <a href='https://data.geographic.texas.gov/order/submit?uuid=%s'>link.</a><br />
                            For questions or concerns, Please reply to this email or visit our <a href='https://tnris.org/contact/'>contact page</a> for more ways to contact TNRIS.<br /><br />
                            Thanks,<br />
                            The TxGIO Team
                            </body></html>
                        """ % str(instance.pk),
                    send_to=order_info["Email"],
                    reply_to=os.environ.get("STRATMAP_EMAIL")
                )
            return Response(
                {"status": "success", "message": "Success"},
                status=status.HTTP_201_CREATED,
            )
        
    def notify_user(self, order_object, email):
        #Notify user
        api_helper_v1.send_email(
            "Your datahub order has been received",
            """
                <html><body style='overflow:hidden'>
            """
            + "<div style='width: 100%; background-color: #1e8dc1; overflow:hidden;'>" +
            """
                    <img class="TnrisLogo" width="100" height="59" src="https://cdn.tnris.org/images/txgio_light.png" alt="TxGIO Logo" title="data.tnris.org">
                    </div><br /><br />
                    Greetings from TxGIO,<br /><br />
                    We have received your order and will process it after taking a look at the details.<br />
                    In the meantime you can check your order status <a href='https://data.geographic.texas.gov/order/status?uuid=%s'>here</a>.<br />
                    You will receive a link via email to pay for the order once we process it.<br /><br />
                    Thanks,<br />
                    The TxGIO Team
                </body></html>
            """ % str(order_object.id),
            send_to=email,
            reply_to=os.environ.get("STRATMAP_EMAIL")
        )

    def get_order_object(self, email, order):
        access_token = email
        salt = secrets.token_urlsafe(32)
        pepper = os.environ.get("ACCESS_PEPPER")
        hash = hashlib.sha256(bytes(access_token + salt + pepper, 'utf8')).hexdigest()
        
        otp = secrets.token_urlsafe(12)

        order_details = OrderDetailsType.objects.create(details=json.dumps(order), 
                                            access_code=hash, 
                                            access_salt=salt, 
                                            otp=hashlib.sha256(bytes(otp + salt + pepper, 'utf8')).hexdigest(),
                                            otp_age=time.time())
        return OrderType.objects.create(order_details=order_details)

    def create_super(self, request, format=None):
        try:
            if api_helper_v1.checkLogger():
                logger.info("running OrderFormViewSet")
            verify_req = api_helper_v1.checkCaptcha(request.data["recaptcha"])
            if json.loads(verify_req.text)["success"]:
                order = request.data

                if "form_id" in request.data and request.data["form_id"] == "order-map":
                    order_object = self.get_order_object(order["Email"], order)

                    formatted = {
                        k.lower().replace(" ", "_"): v for k, v in request.data.items()
                    }
                    formatted["url"] = (
                        request.META["HTTP_REFERER"]
                        if "HTTP_REFERER" in request.META.keys()
                        else request.META["HTTP_HOST"]
                    )
                    formatted["order_uuid"] = order_object.id
                    email_template = EmailTemplate.objects.get(form_id=request.data["form_id"])

                    body = self.compile_email_body(
                        email_template.email_template_body, formatted
                    )
                    # send to ticketing system unless sendpoint has alternative key value in email template record
                    sender = (
                        os.environ.get("MAIL_DEFAULT_TO")
                        if email_template.sendpoint == "default"
                        else formatted[email_template.sendpoint]
                    )
                    
                    replyer = (
                        formatted["email"]
                        if "email" in formatted.keys()
                        else "unknown@tnris.org"
                    )
                    if "name" in formatted.keys():
                        replyer = "%s <%s>" % (formatted["name"], formatted["email"])

                    api_helper_v1.send_raw_email(
                        subject="Map Order Form",
                        body=body,
                        send_to=sender,
                        reply_to= replyer)

                    self.notify_user(order_object, order["Email"])

                    return Response(
                        {"status": "success", "message": "Success"},
                        status=status.HTTP_201_CREATED,
                    )

                else:
                    # Convert to JSON
                    order = request.data["order_details"]

                    # Generate Access Code and one way encrypt it.
                    order_object = self.get_order_object(request.data["pw"], order)

                    formatted = request.data.get('order_details')
                    formatted["url"] = (
                        request.META["HTTP_REFERER"]
                        if "HTTP_REFERER" in request.META.keys()
                        else request.META["HTTP_HOST"]
                    )
                    formatted["order_uuid"] = order_object.id
                    email_template = EmailTemplate.objects.get(form_id='data-tnris-org-order')

                    body = self.compile_email_body(
                        email_template.email_template_body, formatted
                    )
                    # send to ticketing system unless sendpoint has alternative key value in email template record
                    sender = (
                        os.environ.get("MAIL_DEFAULT_TO")
                        if email_template.sendpoint == "default"
                        else formatted[email_template.sendpoint]
                    )
                    replyer = (
                        formatted["Email"]
                        if "Email" in formatted.keys()
                        else "unknown@tnris.org"
                    )
                    if "Name" in formatted.keys():
                        replyer = "%s <%s>" % (formatted["Name"], formatted["Email"])

                    api_helper_v1.send_raw_email(
                        subject="Dataset Order",
                        body=body,
                        send_to=sender,
                        reply_to= replyer)

                    self.notify_user(order_object, order["Email"])

                    return Response(
                        {"status": "success", "message": "Success"},
                        status=status.HTTP_201_CREATED,
                    )
            else:
                return Response(
                    {"status": "failure", "message": "Captcha is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                ) 
        except Exception as e:
            message = "Error creating order: "
            if(settings.DEBUG):
                message = message + str(e)
                if api_helper_v1.checkLogger():
                    logger.error(message)
            return Response(
                {"status": "failure", "message": "internal error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
