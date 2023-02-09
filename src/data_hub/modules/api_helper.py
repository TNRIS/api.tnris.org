import boto3, json, os
from botocore.exceptions import ClientError
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
    email = EmailMessage(subject, body, send_from, [send_to], reply_to=[reply_to])
    email.send(fail_silently=False)
    return