from django.db import models
from modules.api_helper import encrypt_string, decrypt_string
from cryptography.fernet import Fernet, MultiFernet

import os, boto3
client = boto3.client('s3')

from django import forms

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

class CryptoText(models.Model):
    cryptoText = CryptoTextField()