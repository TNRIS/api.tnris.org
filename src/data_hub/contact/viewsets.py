from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, schemas, status, viewsets
from rest_framework.response import Response
from urllib.parse import urlparse
from datetime import datetime, timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.shortcuts import render

import requests, os, json, re, sys, hashlib, secrets, uuid, time

# policy imports
import logging, watchtower
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from modules import api_helper
# Google Drive auth and GoogleSheets api wrapper libraries
import gspread

from .models import CampaignSubscriber, EmailTemplate, SurveyTemplate, OrderType, OrderDetailsType

from .serializers import *


logger = logging.getLogger("errLog")
if os.environ.get("IS_LIVE") == 'true':
    logger.addHandler(watchtower.CloudWatchLogHandler())

CCP_URL = 'https://securecheckout-uat.cdc.nicusa.com/ccprest/api/v1/TX/'
# custom permissions for cors control
class CorsPostPermission(AllowAny):
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
    ]

    def has_permission(self, request, view):
        u = (
            urlparse(request.META["HTTP_REFERER"]).hostname
            if "HTTP_REFERER" in request.META.keys()
            else request.META["HTTP_HOST"]
        )
        return u in self.whitelisted_domains
    
# ######################################################
# ############## CONTACT FORM ENDPOINTS ################
# ######################################################


# FORMS SUBMISSION ENDPOINT
class SubmitFormViewSet(viewsets.ViewSet):
    """
    Handle TNRIS form submissions (Restricted Access)
    """

    permission_classes = [CorsPostPermission]

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

    def create(self, request, format=None):
        # if in DEBUG mode, assume local development and use localhost recaptcha secret
        # otherwise, use product account secret environment variable
        recaptcha_secret = (
            "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
            if settings.DEBUG
            else os.environ.get("RECAPTCHA_SECRET")
        )
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        recaptcha_data = {
            "secret": recaptcha_secret,
            "response": request.data["recaptcha"],
        }
        verify_req = requests.post(url=recaptcha_verify_url, data=recaptcha_data)
        # get email template for form. if bad form, return error
        try:
            email_template = EmailTemplate.objects.get(form_id=request.data["form_id"])
        except:
            return Response(
                {"status": "error", "message": "form_id not registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if recaptcha verification a success, add to database
        if json.loads(verify_req.text)["success"]:
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
                # emails send to supportsystem to create tickets in the ticketing system
                # which are ultimately managed by IS, RDC, and StratMap
                api_helper.send_email(
                    email_template.email_template_subject,
                    body,
                    send_to=sender,
                    reply_to=replyer,
                )
                return Response(
                    {"status": "success", "message": "Form Submitted Successfully!"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "status": "error",
                    "message": "Serializer Save Failed.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"status": "error", "message": "Recaptcha Verification Failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

class GenOtpViewSet(viewsets.ViewSet):
    """
    Regenerate One Time Passcode
    """
    permission_classes = [CorsPostPermission]
    
    def create(self, request, format=None):
        try:
            verify_req = api_helper.checkCaptcha(settings.DEBUG, request.data["recaptcha"])
            if json.loads(verify_req.text)["success"]:

                order = OrderType.objects.get(id=request.query_params["uuid"])
                details = json.loads(order.order_details.details)
                
                # Regenerate OTP
                otp = secrets.token_urlsafe(6)
                salt = order.order_details.access_salt
                pepper = os.environ.get("ACCESS_PEPPER")

                order.order_details.otp = hashlib.sha256(bytes(otp + salt + pepper, 'utf8')).hexdigest()
                order.order_details.otp_age=time.time()
                
                order.order_details.save()
                
                # Send One time passcode to users email.
                api_helper.send_email(
                    subject="DataHub one time passcode",
                    body="Your new one time passcode is: " + otp,
                    send_to=details["Email"]
                )
                
                return Response(
                    {"status": "success", "message": "Placeholder."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "failure", "message": "Captcha is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                ) 
        except Exception as e:
            logger.error("Error generating the One time passcode. Exception: " + str(e))
            return Response(
                {"status": "failure", "message": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )  
    
class OrderStatusViewSet(viewsets.ViewSet):
    """
    Handle Checking the order status
    """
    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            verify_req = api_helper.checkCaptcha(settings.DEBUG, request.data["recaptcha"])
            if json.loads(verify_req.text)["success"]:
                order = OrderType.objects.get(id=request.query_params["uuid"])
                authorized = api_helper.auth_order(request.data, order.order_details)
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
            else:
                return Response(
                    {"status": "failure", "message": "Captcha is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )         
        except Exception as e:
            logger.error("Error checking order status. Exception: " + str(e))
            return Response(
                {"status": "failure", "message": "Order not found. Or order has been processed."},
                status=status.HTTP_404_NOT_FOUND,
            )

class OrderCleanupViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    
    def create(self, request, format=None):
        if(os.environ.get("CCP_ACCESS_CODE")!= request.data):
            return Response(
                {"status": "access_denied", "message": "access_denied"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            # Select all of the orders that are not archived.

            unarchived_orders = OrderType.objects.filter(archived=False).values()
            
            now = datetime.now(timezone.utc)
            
            # If an order is older than 15 days archive it regardless.
            for order in unarchived_orders:
                difference = now - order["created"] 
                temp_req = request
                temp_req.query_params._mutable = True
                temp_req.query_params["uuid"] = str(order["id"])
                temp_req.query_params._mutable = False
                a = self.get_receipt(request, format)
                if(a.status_code == 200):
                    if(not order["tnris_notified"]):
                        obj = OrderType.objects.get(id=order["id"])
                        obj.tnris_notified = True
                        obj.save()
                        api_helper.send_email(subject="Payment has been received.",
                            body="Order uuid: " + str(order["id"]) + " has been received. Please send package according to order details, then complete order.",
                            send_from=os.environ.get("MAIL_DEFAULT_FROM"))    
                        print("pause") 
                    
                #If no receipt was received or order was sent after 15 days then archive order automatically.
                if(difference.days > 15 and (a.status_code != 200 or order["order_sent"] == True) ):
                    obj = OrderType.objects.get(id=order["id"])
                    obj.archived = True
                    obj.save()
                                          
            response =  Response(
                {"status": "success", "message": "success"},
                status=status.HTTP_200_OK,
            )
            # return response
        except:
            logger.error("Error cleaning up orders. Exception: " + str(e))
            response =  Response(
                {"status": "failure", "message": "failure"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            return response
    
    def get_receipt(self, request, format):
        try:
            order = OrderType.objects.get(id=request.query_params["uuid"])
            headers={
                "apiKey": os.environ.get("CCP_API_KEY"),
                "MerchantKey": os.environ.get("CCP_MERCHANT_KEY"),
                "MerchantCode": os.environ.get("CCP_MERCHANT_CODE"),
                "ServiceCode": os.environ.get("CCP_SERVICE_CODE")
            }
            orderinfo = requests.get(CCP_URL + "tokens/" + str(order.order_token), headers=headers) 
            
            orderContent = json.loads(orderinfo.content)
            if('orders' in orderContent):
                orders = orderContent["orders"]
                orderReceipt = requests.get(CCP_URL + "receipts/" + str(orders[0]['orderId']), headers=headers)
                response = Response(
                    {"status_code": orderReceipt.status_code, "orderReceipt": orderReceipt}
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
            logger.error("Error getting receipt: " + str(e))
        finally:
            return response

class OrderSubmitViewSet(viewsets.ViewSet):
    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            verify_req = api_helper.checkCaptcha(settings.DEBUG, request.data["recaptcha"])
            if json.loads(verify_req.text)["success"]:
                orderObj = OrderType.objects
                order = orderObj.get(id=request.query_params["uuid"])
                authorized = api_helper.auth_order(request.data, order.order_details)
                if(not authorized):
                    return Response({"status": "denied",
                                    "order_url": "NONE",
                                    "message": "Access is denied. Either access code is wrong or One time passcode has expired."},
                    status=status.HTTP_403_FORBIDDEN,
                )
                
                order_details = json.loads(order.order_details.details)
                
                item_attributes = json.load(open("itemattributes.json"))
                
                total = order.approved_charge
                
                #2.25% and $.25
                transactionfee = round(((total/100) * 2.25) + .25, 2)
                body = {
                    "OrderTotal": total + transactionfee,
                    "MerchantCode": os.environ.get("CCP_MERCHANT_CODE"),
                    "MerchantKey": os.environ.get("CCP_MERCHANT_KEY"),
                    "ServiceCode": os.environ.get("CCP_SERVICE_CODE"),
                    "UniqueTransId": order.order_details_id,
                    "LocalRef": "580WD" + str(order.order_details_id),
                    "PaymentType": order_details['Payment'],
                    "LineItems": [
                        {
                            "Sku": "DHUB",
                            "Description": "TNRIS DataHub order",
                            "UnitPrice": total + transactionfee,
                            "Quantity": 1,
                            "ItemAttributes": item_attributes
                        }
                    ]
                }
                
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'USAS1', 'FieldValue': total})
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'USAS2', 'FieldValue': transactionfee})
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'USAS3', 'FieldValue': transactionfee})
                body["LineItems"][0]["ItemAttributes"].append({'FieldName':'CONV_FEE', 'FieldValue': transactionfee})
                x = requests.post(
                    CCP_URL + "tokens", 
                    json = body,
                    headers={
                        "apiKey": os.environ.get("CCP_API_KEY")
                    }
                )

                url = json.loads(x.text)
                if('htmL5RedirectUrl' in url):
                    orderObj.filter(id=request.query_params["uuid"]).update(order_token=url["token"], order_url=url["htmL5RedirectUrl"])
                    order = orderObj.get(id=request.query_params["uuid"])

                    #response = redirect(order.order_url)
                    response = Response(
                        {"status": "success", "order_url": order.order_url, "message": "success"}
                    )
                else:
                    response =  Response(
                        {"status": "failure", "order_url": "NONE", "message": "The order has failed"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
            else:
                return Response(
                    {"status": "failure", "message": "Captcha is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )         
        except Exception as e:
            logger.error("Error creating order. Exception: " + str(e))
            response =  Response(
                {"status": "failure", "order_url": "NONE", "message": "The order has failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        return response

# FORMS ORDER ENDPOINT
class OrderFormViewSet(viewsets.ViewSet):
    """
    Handle TNRIS order form submissions
    """
    permission_classes = [CorsPostPermission]

    @receiver(pre_save, sender=OrderType)
    def my_callback(sender, instance, *args, **kwargs):
        instance.order_approved
        if(instance.order_approved and instance.approved_charge):
            order_info = json.loads(instance.order_details.details)
            if(not instance.customer_notified):
                instance.customer_notified = True
                instance.save()
                api_helper.send_email(
                    subject="Your order has been approved",
                    body="Please send payment. \n Url: " + "placeholder",
                    send_to=order_info["Email"],
                    send_from=os.environ.get("MAIL_DEFAULT_FROM")
                )
        return Response(
            {"status": "success", "message": "Success"},
            status=status.HTTP_201_CREATED,
        )
        
    def create(self, request, format=None):
        try:
            logger.error("TESTLOG")
            verify_req = api_helper.checkCaptcha(settings.DEBUG, request.data["recaptcha"])
            if json.loads(verify_req.text)["success"]:

                # Convert to JSON
                order = request.data["order_details"]

                # Generate Access Code and one way encrypt it.
                access_token = request.data["pw"]
                salt = secrets.token_urlsafe(32)
                pepper = os.environ.get("ACCESS_PEPPER")
                hash = hashlib.sha256(bytes(access_token + salt + pepper, 'utf8')).hexdigest()
                
                otp = secrets.token_urlsafe(6)
                
                order_details = OrderDetailsType.objects.create(details=json.dumps(order), 
                                                      access_code=hash, 
                                                      access_salt=salt, 
                                                      otp=hashlib.sha256(bytes(otp + salt + pepper, 'utf8')).hexdigest(),
                                                      otp_age=time.time())
                order_object = OrderType.objects.create(order_details=order_details)

                api_helper.send_email("Your TNRIS Order Details", '\nYour order ID is: ' + str(order_object.id)
                                + '\nYou can check your order status here ' + "placeholder"
                                + '\n\nYou will receive a link via email to pay for the order once we process it.',
                                send_to=order["Email"])

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
            logger.error("Error creating order: " + str(e))
            return Response(
                {"status": "failure", "message": "internal error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# POLICY ENDPOINTS FOR UPLOADS
def create_presigned_post(key, content_type, length, expiration=900):
    """Generate a presigned URL S3 POST request to upload a file

    :param key: string
    :param content_type: string
    :param length: integer
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid. default 15min
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    bucket = os.environ.get("S3_UPLOAD_BUCKET")
    fields = {
        "acl": "private",
        "Content-Type": content_type,
        "Content-Length": length,
        "success_action_status": "201",
        "success_action_redirect": "",
    }
    # if in conditions array, must be in fields dictionary and client
    # side form inputs/fields as well
    conditions = [
        {"acl": "private"},
        ["starts-with", "$success_action_status", ""],
        ["starts-with", "$success_action_redirect", ""],
        ["starts-with", "$key", ""],
        ["starts-with", "$Content-Type", content_type],
        ["starts-with", "$Content-Length", ""],
        ["content-length-range", 1, length],
    ]
    # Generate a presigned S3 POST URL
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("S3_UPLOAD_KEY"),
        aws_secret_access_key=os.environ.get("S3_UPLOAD_SECRET"),
        config=Config(signature_version="s3v4"),
    )
    try:
        response = s3_client.generate_presigned_post(
            bucket, key, Fields=fields, Conditions=conditions, ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


class ZipPolicyViewSet(viewsets.ViewSet):
    """
    Get client form zipfile presigned url for s3 (Restricted Access)
    """

    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            presigned = create_presigned_post(
                request.data["key"], "application/zip", 20971520
            )  # 20MB
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(presigned, status=status.HTTP_201_CREATED)


class ImagePolicyViewSet(viewsets.ViewSet):
    """
    Get client form image presigned url for s3 (Restricted Access)
    """

    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            presigned = create_presigned_post(
                request.data["key"], "image", 5242880
            )  # 5MB
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(presigned, status=status.HTTP_201_CREATED)


class FilePolicyViewSet(viewsets.ViewSet):
    """
    Get client form generic file presigned url for s3 (Restricted Access)
    """

    permission_classes = [CorsPostPermission]

    def create(self, request, format=None):
        try:
            presigned = create_presigned_post(request.data["key"], "", 5242880)  # 5MB
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(presigned, status=status.HTTP_201_CREATED)


# ######################################################
# ################## SURVEY ENDPOINTS ##################
# ######################################################


# SURVEY DELIVERY
class SurveyTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve surveys to deliver survey modal content to front-end
    """

    serializer_class = SurveyTemplateSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        # only return latest public survey record
        args = {"public": True}

        # get records using query
        queryset = SurveyTemplate.objects.filter(**args).order_by("-last_modified")
        return queryset


# SURVEY SUBMISSION
class SubmitSurveyViewSet(viewsets.ViewSet):
    """
    Handle generic SurveyJS survey submissions (Restricted Access)
    """

    permission_classes = [CorsPostPermission]

    def flatten_json_recursively(self, y):
        out = {}

        def flatten(x, name=""):
            # If the Nested key-value
            # pair is of dict type
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + "_")
            # If the Nested key-value
            # pair is of list type
            elif type(x) is list:
                i = 0

                for a in x:
                    flatten(a, name + str(i) + "_")
                    i += 1

            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    def submit_to_google_sheet(self, sheet_id, flattened_survey_response):
        # Reliably set current path location
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__)))
        )

        # Get credentials and authenticate using gspread auth wrapper and __location__
        try:
            gc = gspread.service_account(
                filename=os.path.join(__location__, "gspread_config.json")
            )
        except Exception as e:
            return Response({"status": "error", "message": "GSpread auth unsuccessful" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Open spreadsheet by url using request.data['sheet_id']
        try:
            SHEET = gc.open_by_key(sheet_id)
        except Exception as e:
            return Response({"status": "error", "message": "GSpread sheet retreival unsuccessful" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get current headers values
        try:
            current_headers = SHEET.get_worksheet(0).row_values(1)
        except Exception as e:
            return Response({"status": "error", "message": "GSpread headers retreival unsuccessful" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get row index for the end of the spreadsheet
        try: 
            next_empty_row = len(SHEET.get_worksheet(0).col_values(1)) + 1
        except Exception as e:
            return Response({"status": "error", "message": "GSpread next_empty_row unsuccessful" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        submitted_values = flattened_survey_response

        # Variable to store new row values
        new_row = []
        # Variable to store new header values
        new_headers = current_headers

        # Cycle through current header fields
        # If the existing field was sent, add its designated column
        ## Pop value from list so that only submitted values which do not have columns remain in submitted_values
        # If current header exists in Sheet but was not sent in request, mark value as empty string
        for v in current_headers:
            if v in submitted_values:
                new_row.append(submitted_values.pop(v))
            else:
                new_row.append("")

        # Cycle through remaining submitted_values as 2D array
        for remaining in submitted_values.items():
            # Append unique header / field key to first row of table (column names)
            new_headers.append(remaining[0])
            # Append value belonging to unique key to new row of table
            new_row.append(remaining[1])

        # Use batch_update to reduce HTTP calls
        try: 
            SHEET.get_worksheet(0).batch_update(
            [
                # UPDATE SHEET, adding new header row to sheet
                {"range": "A1", "values": [new_headers]},
                # UPDATE SHEET, adding new row to sheet
                {
                    # Must use gspread.utils to convert row index # to 'A1' style notation
                    # Must use ternary on next_empty_row so that it will not overwrite header on first submission
                    "range": gspread.utils.rowcol_to_a1(
                        2 if next_empty_row == 1 else next_empty_row, 1
                    ),
                    "values": [new_row],
                },
            ]
        )
        except Exception as e:
            return Response({"status": "error", "message": "GSpread batch_update unsuccessful" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, format=None):

        resp = request.data["survey_response"]
        sheet = request.data["sheet_id"]
        # Flatten json request data
        try:
            flat = self.flatten_json_recursively(resp)
        except Exception as e:
            return Response({"status": "error", "message": "Error while flattening response data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Submit to Google Spreadsheet
        self.submit_to_google_sheet(sheet, flat)

        return Response(
            {"status": "success", "message": "Survey submitted successfully"},
            status=status.HTTP_201_CREATED,
        )

# Orders GET endpoint READ_ONLY
class DataHubOrdersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Retrieve TNRIS DataHub Order submissions
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DataHubOrderSerializer
    http_method_names = ['get']

    def get_queryset(self):
        args = {}
        null_list = ['null', 'Null', 'none', 'None']
        # create argument object of query clauses
        for field in self.request.query_params.keys():
            if field != 'limit' and field != 'offset':
                value = self.request.query_params.get(field)
                # convert null queries
                if value in null_list:
                    value = None
                args[field] = value
        # get records using query
        queryset = DataHubOrder.objects.filter(**args)
        return queryset

# Campaigns rw endpoint
class SubmitCampaignSubscriptionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    post:
    Create email campaign subscriptions
    """
    queryset = CampaignSubscriber.objects.all()
    serializer_class = CampaignSubscriberSerializer
    permission_classes = [CorsPostPermission]
    schema = schemas.AutoSchema()
    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)