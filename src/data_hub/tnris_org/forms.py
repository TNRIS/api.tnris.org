from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget

from string import Template
from django.utils.safestring import mark_safe

from django.db.utils import ProgrammingError
from .models import (TnrisImage, TnrisDocument)
import os
import boto3, uuid


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<input type="file" name="$name" id="id_$name"><label for="img_$name">Current: <a href="$link" target="_blank">$link</a></label><img id="img_$name" src="$link"/>""")
        return mark_safe(html.substitute(link=value,name=name))


class DocumentWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<input type="file" name="$name" id="id_$name"><label for="doc_$name">Current: <a href="$link">$link</a></label>""")
        return mark_safe(html.substitute(link=value,name=name))


class ImageForm(forms.ModelForm):
    class Meta:
        model = TnrisImage
        fields = ('__all__')

    image_url = forms.FileField(required=False, widget=PictureWidget, help_text="Choose an image file and 'Save' this form to upload & save it to the database. Attempting to overwrite with a new file will only create a new record.")

    # boto3 s3 object
    client = boto3.client('s3')

    # function to upload image to s3 and update dbase link
    def handle_image(self, field, file):
        # upload image
        key = "images/%s" % (file)
        response = self.client.put_object(
            Bucket='tnris-org-static',
            ACL='public-read',
            ContentType='image',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        setattr(self.instance, field, "https://tnris-org-static.s3.amazonaws.com/" + key)
        setattr(self.instance, "image_name", str(file))
        return

    # custom handling of images on save method
    def save(self, commit=True):
        # check for files
        files = self.files
        # if files and field not marked for deletion then upload to s3
        for f in files:
            print(f)
            ext = os.path.splitext(str(files[f]))[1]
            valid_extensions = ['.jpg', '.png', '.gif', '.jpeg', '.svg']
            print(ext)
            if not ext.lower() in valid_extensions:
                raise ValidationError(u"Unsupported file extension. Only .jpg, .png, .gif, and .jpeg file extensions supported for Tnris Images")

            self.handle_image(f, files[f])

        return super(ImageForm, self).save(commit=commit)


class DocumentForm(forms.ModelForm):
    class Meta:
        model = TnrisDocument
        fields = ('__all__')

    document_url = forms.FileField(required=False, widget=DocumentWidget, help_text="Choose a document file and 'Save' this form to upload & save it to the database. Attempting to overwrite with a new file will only create a new record.")

    # boto3 s3 object
    client = boto3.client('s3')

    # function to upload document to s3 and update dbase link
    def handle_doc(self, field, file):
        # upload image
        key = "documents/%s" % (file)
        response = self.client.put_object(
            Bucket='tnris-org-static',
            ACL='public-read',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        setattr(self.instance, field, "https://tnris-org-static.s3.amazonaws.com/" + key)
        setattr(self.instance, "document_name", str(file))
        return

    # custom handling of documents on save method
    def save(self, commit=True):
        # check for files
        files = self.files
        # if files and field not marked for deletion then upload to s3
        for f in files:
            ext = os.path.splitext(str(files[f]))[1]
            invalid_extensions = ['.jpg', '.png', '.gif', '.jpeg', '.svg']
            print(ext)
            if ext.lower() in invalid_extensions:
                raise ValidationError(u"Unsupported file extension. All images should be uploaded using 'Tnris Images'.")

            self.handle_doc(f, files[f])

        return super(DocumentForm, self).save(commit=commit)
