from django.db import models

from cryptography.fernet import Fernet, MultiFernet
from botocore.exceptions import ClientError

import boto3, json

from django import forms

# widget stuff
from django.forms import widgets

class CountableWidget(widgets.Textarea):
    pass

class CryptoTextField(models.Field):
    description = "A crypto field"
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['null'] = True

        super().__init__(*args, **kwargs)
        
    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.TimeField,
            **kwargs,
        })
        #return models.Field.formfield(self, models.BooleanField, **kwargs)
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["blank"]
        del kwargs["null"]
        return name, path, args, kwargs
    
    def get_prep_value(self, value):
        return encrypt_string(value) 

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_string(value)
    
    def to_python(self, value):
        if isinstance(value, CryptoText):
            return value
        if value is None:
            return value
        return decrypt_string(value)
  

def encrypt_string(value): 
    access_key = bytes(json.loads(get_access_key())["fkey1"], 'utf-8')
    f = Fernet(access_key)
    if(value):
        encrypted = f.encrypt(bytes(value, 'utf-8'))
    else:
        encrypted = f.encrypt(bytes("", 'utf-8'))    
    return encrypted

def decrypt_string(value): 
    access_key = bytes(json.loads(get_access_key())["fkey1"], 'utf-8')
    f = Fernet(access_key)    
    decrypted = f.decrypt(bytes(value))
    
    return decrypted.decode('utf-8')

def get_access_key():
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId='datahub_order_keys'
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return secret

class CryptoText(models.Model):
    cryptoText = CryptoTextField()