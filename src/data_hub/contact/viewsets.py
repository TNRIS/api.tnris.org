"""
Contact viewset
"""
from urllib.parse import urlparse
import os
import logging
import watchtower

from django.shortcuts import redirect

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, schemas, status, viewsets
from rest_framework.response import Response
from contact import fiserv_payments
from contact import ccp_payments

import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from modules import api_helper
# Google Drive auth and GoogleSheets api wrapper libraries
import gspread

from .models import CampaignSubscriber, SurveyTemplate

from .serializers import (
    SurveyTemplateSerializer,
    DataHubOrderSerializer,
    CampaignSubscriberSerializer)

logger = logging.getLogger("errLog")
logger.addHandler(watchtower.CloudWatchLogHandler())

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

# ######################################################
# ################### CCP ENDPOINTS ####################
# ######################################################

class CcpSubmitFormViewSet(ccp_payments.SubmitFormViewSetSuper):
    """
    Old submit form, will be deprecated soon.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Running CcpSubmitFormViewSet")

class CcpGenOtpViewSet(ccp_payments.GenOtpViewSetSuper):
    """
    Generate One time password viewset for CCP.
    """
    permission_classes = [CorsPostPermission]

    def create(self, request):
        return self.captcha_intro(request, "Regenerating one time passcode. CcpGenOtpViewSet.")

class CcpOrderStatusViewSet(ccp_payments.OrderStatusViewSetSuper):
    """
    Order Status viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "running CcpOrderStatusViewSet")

class CcpInitiateRetentionCleanupViewSet(ccp_payments.InitiateRetentionCleanupViewSetSuper):
    """
    Initiate retention cleanup viewset for ccp.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
       return self.intro(request, "running CcpInitiateRetentionCleanupViewSet")

class CcpOrderCleanupViewSet(ccp_payments.OrderCleanupViewSetSuper):
    """
    Order cleanup viewset.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
        return self.intro(request, "running CcpOrderCleanupViewSet")

class CcpOrderSubmitViewSet(ccp_payments.OrderSubmitViewSetSuper):
    """
    CCP Order submit viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.intro(request, "Starting CcpOrderSubmitViewSet")

class CcpOrderFormViewSet(ccp_payments.OrderFormViewSetSuper): 
    """
    Ccp Order form viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.intro(request, "running CcpOrderFormViewSet")
    
# ######################################################
# ################# FiServ ENDPOINTS ###################
# ######################################################

class FiservSubmitFormViewSet(viewsets.ViewSet):
    """
    Handle TxGIO form submissions (Restricted Access).
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        # Check Recaptcha return if it fails.
        return Response("Endpoint deprecated", status=status.HTTP_410_GONE)

class FiservGenOtpViewSet(fiserv_payments.GenOtpViewSetSuper):
    """
    Generate One time password viewset.
    """
    permission_classes = [CorsPostPermission]

    def create(self, request):
        return self.captcha_intro(request, "Regenerating one time passcode. GenOtpViewSet.")

class FiservOrderStatusViewSet(fiserv_payments.OrderStatusViewSetSuper):
    """
    Order Status viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Running OrderStatusViewSet.")

class FiservInitiateRetentionCleanupViewSet(fiserv_payments.InitiateRetentionCleanupViewSetSuper):
    """
    Initiate retention cleanup viewset.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
       return self.intro(request, "running InitiateRetentionCleanupViewSet")

class FiservOrderCleanupViewSet(fiserv_payments.OrderCleanupViewSetSuper):
    """
    Order cleanup viewset.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
        return self.intro(request, "running OrderCleanupViewSet")

class FiservOrderSubmitViewSet(fiserv_payments.OrderSubmitViewSetSuper):
    """
    Order submit viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Starting OrderSubmitViewSet.")

class FiservOrderFormViewSet(fiserv_payments.OrderFormViewSetSuper):
    """
    Order form viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Running OrderFormViewSet.")

class FiservRedirectUrlViewSet(viewsets.ViewSet):
    """
    Redirect to a url.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        # Redirect
        return redirect("https://data.geographic.texas.gov/order/redirect?status=success")

# ######################################################
# ################## ORDER ENDPOINTS ###################
# ######################################################

# ######################################################
# ################### CCP ENDPOINTS ####################
# ######################################################

class CcpSubmitFormViewSet(ccp_payments.SubmitFormViewSetSuper):
    """
    Old submit form, will be deprecated soon.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Running CcpSubmitFormViewSet")

class CcpGenOtpViewSet(ccp_payments.GenOtpViewSetSuper):
    """
    Generate One time password viewset for CCP.
    """
    permission_classes = [CorsPostPermission]

    def create(self, request):
        return self.captcha_intro(request, "Regenerating one time passcode. CcpGenOtpViewSet.")

class CcpOrderStatusViewSet(ccp_payments.OrderStatusViewSetSuper):
    """
    Order Status viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "running CcpOrderStatusViewSet")

class CcpInitiateRetentionCleanupViewSet(ccp_payments.InitiateRetentionCleanupViewSetSuper):
    """
    Initiate retention cleanup viewset for ccp.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
       return self.intro(request, "running CcpInitiateRetentionCleanupViewSet")

class CcpOrderCleanupViewSet(ccp_payments.OrderCleanupViewSetSuper):
    """
    Order cleanup viewset.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
        return self.intro(request, "running CcpOrderCleanupViewSet")

class CcpOrderSubmitViewSet(ccp_payments.OrderSubmitViewSetSuper):
    """
    CCP Order submit viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.intro(request, "Starting CcpOrderSubmitViewSet")

class CcpOrderFormViewSet(ccp_payments.OrderFormViewSetSuper): 
    """
    Ccp Order form viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.intro(request, "running CcpOrderFormViewSet")
    
# ######################################################
# ################# FiServ ENDPOINTS ###################
# ######################################################

class FiservSubmitFormViewSet(viewsets.ViewSet):
    """
    Handle TxGIO form submissions (Restricted Access).
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        # Check Recaptcha return if it fails.
        return Response("Endpoint deprecated", status=status.HTTP_410_GONE)

class FiservGenOtpViewSet(fiserv_payments.GenOtpViewSetSuper):
    """
    Generate One time password viewset.
    """
    permission_classes = [CorsPostPermission]

    def create(self, request):
        return self.captcha_intro(request, "Regenerating one time passcode. GenOtpViewSet.")

class FiservOrderStatusViewSet(fiserv_payments.OrderStatusViewSetSuper):
    """
    Order Status viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Running OrderStatusViewSet.")

class FiservInitiateRetentionCleanupViewSet(fiserv_payments.InitiateRetentionCleanupViewSetSuper):
    """
    Initiate retention cleanup viewset.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
       return self.intro(request, "running InitiateRetentionCleanupViewSet")

class FiservOrderCleanupViewSet(fiserv_payments.OrderCleanupViewSetSuper):
    """
    Order cleanup viewset.
    """
    permission_classes = (AllowAny,)
    def create(self, request):
        return self.intro(request, "running OrderCleanupViewSet")

class FiservOrderSubmitViewSet(fiserv_payments.OrderSubmitViewSetSuper):
    """
    Order submit viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Starting OrderSubmitViewSet.")

class FiservOrderFormViewSet(fiserv_payments.OrderFormViewSetSuper):
    """
    Order form viewset.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        return self.captcha_intro(request, "Running OrderFormViewSet.")

class FiservRedirectUrlViewSet(viewsets.ViewSet):
    """
    Redirect to a url.
    """
    permission_classes = [CorsPostPermission]
    def create(self, request):
        # Redirect
        return redirect("https://data.geographic.texas.gov/order/redirect?status=success")

# ######################################################
# ################## ORDER ENDPOINTS ###################
# ######################################################
class SubmitFormViewSet(SubmitFormViewSetSuper):
    """
    Handle TxGIO form submissions (Restricted Access).
    """
    def create(self, request):
        # Check Recaptcha return if it fails.
        verify_req = api_helper.checkCaptcha(request.data["recaptcha"])
        if not json.loads(verify_req.text)["success"]:
            return self.build_error_response("Recaptcha Verification Failed.")
        
        super().create(self, request)

class GenOtpViewSet(GenOtpViewSetSuper):
    """
    Generate One time password viewset.
    """

class OrderStatusViewSet(OrderStatusViewSetSuper):
    """
    Order Status viewset.
    """

class InitiateRetentionCleanupViewSet(InitiateRetentionCleanupViewSetSuper):
    """
    Initiate retention cleanup viewset.
    """

class OrderCleanupViewSet(OrderCleanupViewSetSuper):
    """
    Order cleanup viewset.
    """

class OrderSubmitViewSet(OrderSubmitViewSetSuper):
    """
    Order submit viewset.
    """

class OrderFormViewSet(OrderFormViewSetSuper):
    """
    Order form viewset.
    """

# ######################################################
# ############## CONTACT FORM ENDPOINTS ################
# ######################################################
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
        if api_helper.checkLogger():
            logger.error(e)
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
    Retrieve TxGIO DataHub Order submissions
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
