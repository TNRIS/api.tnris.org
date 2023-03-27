from django.db import models

from cryptography.fernet import Fernet, MultiFernet

import os, boto3
from io import BytesIO
import logging, watchtower

logger = logging.getLogger("errLog")
logger.addHandler(watchtower.CloudWatchLogHandler())
client = boto3.client('s3')

from django import forms

# widget stuff
from django.forms import widgets

class CountableWidget(widgets.Textarea):
    pass

class CryptoTextField(models.CharField):
    description = "A crypto field"
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['max_length'] = 50000
        super().__init__(*args, **kwargs)
        
    def db_type(self, connection):
        return 'char(50000)'    
    
    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.CharField,
            **kwargs,
        })
        #return models.Field.formfield(self, models.BooleanField, **kwargs)
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["blank"]
        del kwargs["null"]
        del kwargs["max_length"]
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
    access_key = bytes(os.environ.get("FKEY1"), 'utf-8')
    f = Fernet(access_key)
    if(value):
        encrypted = f.encrypt(bytes(value, 'utf-8'))
    else:
        encrypted = f.encrypt(bytes("", 'utf-8'))    
    return encrypted.decode('utf-8')

def decrypt_string(value): 
    access_key = bytes(os.environ.get("FKEY1"), 'utf-8')
    f = Fernet(access_key)    
    decrypted = f.decrypt(bytes(value, 'utf-8'))
    
    return decrypted.decode('utf-8')

class ProtectedImageField(models.Field):
    try:
        description = "A field that can read from a protected S3 bucket."

        def __init__(self, *args, **kwargs):
            kwargs['max_length'] = 104
            super().__init__(*args, **kwargs)

        def db_type(self, connection):
            return 'varchar(254)'    

        #Store image in protected S3
        def get_prep_value(self, value):
            return value

        #Read image from protected S3
        def from_db_value(self, value, expression, connection):
            if(len(value) > 0):
                session = boto3.Session()
                s3_client = session.client("s3")

                f = BytesIO()
                s3_client.download_fileobj("contact-uploads-private", value, f)

                return list(f.getvalue())
            else:
                return ""
    except Exception as e:
        logger.error(str(e))


class CryptoText(models.Model):
    cryptoText = CryptoTextField()