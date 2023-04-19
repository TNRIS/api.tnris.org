import boto3, json, os, hashlib, time, requests
from botocore.exceptions import ClientError
from django.core.mail import send_mail
from django.core.mail import EmailMessage


def get_secret(secret_name):
    """ Access all of the AWS Secrets via it's Identifier.

    Args:
        secret_name (string): Name of the Secret in AWS secrets manager

    Raises:
        e: ClientError thrown from AWS

    Returns:
        object: A Object that contains all of the Secrets for a particular secret group.
    """
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    return json.loads(get_secret_value_response['SecretString'])

def send_email(
        subject,
        body,
        send_from=os.environ.get("MAIL_DEFAULT_FROM"),
        send_to=os.environ.get("MAIL_DEFAULT_TO"),
        reply_to="unknown@tnris.org",
    ):
    """ Generic function for sending emails from the API

    Args:
        subject (String): Subject header for the email
        body (String): Email Body
        send_from (String, optional): Email to send from.. Defaults to os.environ.get("MAIL_DEFAULT_FROM").
        send_to (_type_, optional): Email Address to receive.. Defaults to os.environ.get("MAIL_DEFAULT_TO").
        reply_to (str, optional): Email address to reply to.. Defaults to "unknown@tnris.org".
    """

    send_mail(subject, body, send_from, [send_to], html_message=body)
    return

def send_raw_email(
    subject,
    body,
    send_from=os.environ.get("MAIL_DEFAULT_FROM"),
    send_to=os.environ.get("MAIL_DEFAULT_TO"),
    reply_to="unknown@tnris.org",
):
    email = EmailMessage(subject, body, send_from, [send_to], reply_to=[reply_to])
    email.send(fail_silently=False)
    return

def auth_order(auth_details, order):
    """Compare hashes of access code and one time passcode

    Args:
        auth_details (python object): Body of request sent in from datahub containing access code and otp
        order_details (python object): Order details from order_details_type

    Returns:
        boolean: Whether access is denied or allowed.
    """
    try:
        order_details = order.order_details
        #Gather access token and One time passcode
        access_token = auth_details["accessCode"]
        otp = auth_details["passCode"]
        
        # Secret salt to stop rainbow tables
        salt = order_details.access_salt
        
        # Secret pepper to stop rainbow tables even if salt is known.
        pepper = os.environ.get("ACCESS_PEPPER")
        
        # Hash auth_details
        ac_hash = hashlib.sha256(bytes(access_token + salt + pepper, 'utf8')).hexdigest()
        otp_hash = hashlib.sha256(bytes(otp + salt + pepper, 'utf8')).hexdigest()
        
        # How old in seconds is our otp?
        otp_age_seconds = time.time() - order_details.otp_age
        
        # Compare with our stored hash.
        ACCESS_CODE_VALID = ac_hash == order_details.access_code
        
        # Compare with stored hash and ensure it's not more than 15 minutes old
        OTP_VALID = otp_hash == order_details.otp and otp_age_seconds < 1800
    except Exception as e:
        return False
    if(ACCESS_CODE_VALID and OTP_VALID):
        #Invalidate access code after first success.
        order.order_details.otp_age = 0
        order.order_details.save()
        order.save()
    return ACCESS_CODE_VALID and OTP_VALID

def checkCaptcha(IS_DEBUG, captcha):
    """Check a captcha string for success.

    Args:
        IS_DEBUG (boolean): Whether we are running in debug mode.
        captcha (_type_): String sent in request body to check captcha success/failure

    Returns:
        _type_: python object with information about status of captcha.
    """
    # if in DEBUG mode, assume local development and use localhost recaptcha secret
    # otherwise, use product account secret environment variable
    recaptcha_secret = (
        "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
        if True
        else os.environ.get("RECAPTCHA_SECRET")
    )
    recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
    recaptcha_data = {
        "secret": recaptcha_secret,
        "response": captcha,
    }
    
    return requests.post(url=recaptcha_verify_url, data=recaptcha_data)

def buildOrderString(id, order_obj): 
    order_string = ""
    order_string += "Order ID: " + (id + "\n\n" )
    order_string += "Name: " + (order_obj["Name"] + "\n" if "Name" in order_obj else "\n")
    order_string += "Email: " + (order_obj["Email"] + "\n" if "Email" in order_obj else "\n")
    order_string += "Phone: " + (order_obj["Phone"] + "\n" if "Phone" in order_obj else "\n")
    order_string += "Address: " + (order_obj["Address"] + "\n" if "Address" in order_obj else "\n")
    order_string += "Organization: " + (order_obj["Organization"] + "\n" if "Organization" in order_obj else "\n")
    order_string += "Industry: " + (order_obj["Industry"] + "\n" if "Industry" in order_obj else "\n")
    order_string += "-------------------------------------------------------------------\n"
    order_string += "Hard Drive: " + (order_obj["HardDrive"] + "\n" if "HardDrive" in order_obj else "\n")
    order_string += "Delivery: " + (order_obj["Delivery"] + "\n" if "Delivery" in order_obj else "\n")
    order_string += "Payment: " + (order_obj["Payment"] + "\n" if "Payment" in order_obj else "\n")
    order_string += "-------------------------------------------------------------------\n"
    order_string += "Notes: " + (order_obj["Notes"] + "\n" if "Notes" in order_obj else "\n")
    order_string += ("Fedex ID: " + order_obj["Fedex"] + "\n" if "Fedex" in order_obj and len(order_obj["Fedex"].strip()) > 0 else "\n")
    order_string += "\n"
    order_string += "-------------------------------------------------------------------\n"
    
    try:
        order_string += "Order \n " + order_obj["Order"]
    except:
        order_string += ""

    return order_string