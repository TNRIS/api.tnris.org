from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget

from string import Template
from django.utils.safestring import mark_safe

from django.db.utils import ProgrammingError
from .models import (TnrisImageUrl, TnrisDocUrl)
import os
import boto3, uuid


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<input type="file" name="$name" id="id_$name"><label for="img_$name">Current: $link</label><img id="img_$name" src="$link"/>""")
        return mark_safe(html.substitute(link=value,name=name))


class DocumentWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<input type="file" name="$name" id="id_$name"><label for="doc_$name">Current: $link</label><a href=""""")


class ImageForm(forms.ModelForm):
    class Meta:
        model = TnrisImageUrl
        fields = ('__all__')

    image_url = forms.FileField(required=True, widget=PictureWidget, help_text="Choose an image file and 'Save' this form to upload & save it to the database. Attempting to overwrite with a new file will only create a new record.")

    # generic function to upload image and update dbase link
    def handle_image(self, field, file):
        # upload image
        key = "%s/assets/%s" % (self.instance.collection_id, field.replace('_image', '.jpg'))
        response = self.client.put_object(
            Bucket='tnris-org-static',
            ACL='public-read',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        setattr(self.instance, field, "https://s3.amazonaws.com/data.tnris.org/" + key)
        return

    # custom handling of various relationships on save method
    def save(self, commit=True):
        # check for files
        files = self.files
        # if files and field not marked for deletion then upload to s3
        for f in files:
            delete_checkbox = 'delete_' + f
            if f in image_fields and self.cleaned_data[delete_checkbox] is False:
                self.handle_image(f, files[f])

        return super(CollectionForm, self).save(commit=commit)


class DocForm(forms.ModelForm):
    class Meta:
        model = TnrisDocUrl
        fields = ('__all__')

    doc_url = forms.FileField(required=True, widget=DocumentWidget, help_text="Choose a document file and 'Save' this form to upload & save it to the database. Attempting to overwrite with a new file will only create a new record.")
