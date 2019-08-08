from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget

from string import Template
from django.utils.safestring import mark_safe

from django.db.utils import ProgrammingError
from .models import (TnrisImage, TnrisDocument, TnrisTraining, TnrisForumTraining, TnrisInstructor)
import os
import boto3, uuid


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        js = """
        <script type="text/javascript">
            function copyFunction() {
                var copyText = document.getElementById("currentUrl");
                copyText.select();
                document.execCommand("copy");
            }
        </script>
        """

        if value is None:
            html = Template("""<input type="file" name="$name" id="id_$name"><label for="img_$name">Current: <a href="#">$link</a></label>""")
        else:
            html = Template("""{0}<input type="file" name="$name" id="id_$name" disabled><a style="cursor:pointer;border:solid 1px;padding:3px;margin-left:15px;" onclick="copyFunction();">COPY URL</a><input style="width:50%;margin-left:5px;" type="text" id="currentUrl" value="$link" readonly><br><img id="img_$name" src="$link"/>""".format(js))
        return mark_safe(html.substitute(link=value,name=name))


class DocumentWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        js = """
        <script type="text/javascript">
            function copyFunction() {
                var copyText = document.getElementById("currentUrl");
                copyText.select();
                document.execCommand("copy");
            }
        </script>
        """

        if value is None:
            html = Template("""<input type="file" name="$name" id="id_$name"><label for="doc_$name">Current: <a href="#">$link</a></label>""")
        else:
            html = Template("""{0}<input type="file" name="$name" id="id_$name" disabled><a style="cursor:pointer;border:solid 1px;padding:3px;margin-left:15px;" onclick="copyFunction();">COPY URL</a><input style="width:50%;margin-left:5px;" type="text" id="currentUrl" value="$link" readonly><br><embed style="max-width:80%;max-height:600px;" src="$link"></embed>""".format(js))
        return mark_safe(html.substitute(link=value,name=name))


class HeadshotWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            html = Template("""<input type="text" name="$name" id="id_$name" style="width:758px;"></input>""")
        else:
            html = Template("""<input type="text" name="$name" id="id_$name" style="width:758px;"></input><br><label for="img_$name">Current: <a href="$link" target="_blank">$link</a></label><img id="img_$name" src="$link"/>""")
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
        self.cleaned_data = self.instance.__dict__
        return

    # custom handling of images on save
    def clean(self, commit=True):
        # check for files
        files = self.files
        for f in files:
            print(str(files[f]))
            ext = os.path.splitext(str(files[f]))[1]
            valid_extensions = ['.jpg', '.png', '.gif', '.jpeg', '.svg']
            # validation to prevent non-standard image formats or other files from being uploaded
            if not ext.lower() in valid_extensions:
                raise ValidationError(u"Unsupported file extension. Only .jpg, .png, .gif, and .jpeg file extensions supported for Tnris Images")
            # validation to check if image file name already exists in database
            name_set = TnrisImage.objects.filter(image_name=str(files[f]))
            if len(name_set) > 0:
                raise ValidationError(u"Image file name already exists. Rename your file.")

            self.handle_image(f, files[f])

        super(ImageForm, self).save(commit=commit)
        return



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
        self.cleaned_data = self.instance.__dict__
        return

    # custom handling of documents on save
    def clean(self, commit=True):
        # check for files
        files = self.files
        for f in files:
            print(str(files[f]))
            ext = os.path.splitext(str(files[f]))[1]
            invalid_extensions = ['.jpg', '.png', '.gif', '.jpeg', '.svg']
            # validation to prevent image formats from being uploaded
            if ext.lower() in invalid_extensions:
                raise ValidationError(u"Unsupported file extension. All images should be uploaded to 'Tnris Images', only document type files should be uploaded here.")
            # validation to check if document file name already exists in database
            name_set = TnrisDocument.objects.filter(document_name=str(files[f]))
            if len(name_set) > 0:
                raise ValidationError(u"Document file name already exists. Rename your file.")

            self.handle_doc(f, files[f])

        super(DocumentForm, self).save(commit=commit)
        return


class TnrisTrainingForm(forms.ModelForm):
    class Meta:
        model = TnrisTraining
        fields = ('__all__')

    start_date_time = forms.DateTimeField(help_text="Accepted date and time input formats: '10/25/06 14:30', '10/25/2006 14:30', '2006-10-25 14:30'")
    end_date_time = forms.DateTimeField(help_text="Accepted date and time input formats: '10/25/06 14:30', '10/25/2006 14:30', '2006-10-25 14:30'")
    cost = forms.DecimalField(help_text="Example of accepted formats for training cost: '50.00', '999', '99.99'. Max of 6 digits and 2 decimal places.")
    registration_open = forms.BooleanField(required=False, help_text="Check the box to change registration to open. Default is unchecked.")
    public = forms.BooleanField(required=False, help_text="Check the box to make this training record visible on the website. Default is unchecked.")


class TnrisForumTrainingForm(forms.ModelForm):
    class Meta:
        model = TnrisForumTraining
        fields = ('__all__')

    start_date_time = forms.DateTimeField(help_text="Accepted date and time input formats: '10/25/06 14:30', '10/25/2006 14:30', '2006-10-25 14:30'")
    end_date_time = forms.DateTimeField(help_text="Accepted date and time input formats: '10/25/06 14:30', '10/25/2006 14:30', '2006-10-25 14:30'")
    # training_instructor = forms.MultipleChoiceField(required=True, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple instructors',}), choices=[], help_text="Select all instructors that will be participating in the training.")
    cost = forms.DecimalField(help_text="Example of accepted formats for training cost: '50.00', '999', '99.99'. Max of 6 digits and 2 decimal places.")
    registration_open = forms.BooleanField(required=False, help_text="Check the box to change registration to open. Default is unchecked.")
    public = forms.BooleanField(required=False, help_text="Check the box to make this training record visible on the website. Default is unchecked.")
    max_students = forms.IntegerField(required=False, help_text="Enter max number of students for class room.")


    # general function to create a form dropdown for instructors
    def instructor_choices(self, id_field, label_field, type_table, order_field):
        # get the relate type choices from the type table
        try:
            choices = (
                (b, getattr(b, label_field)) for b in type_table.objects.all().order_by(order_field))
        except ProgrammingError:
            choices = ()
        return choices

    # on instance construction fire functions to retrieve initial values
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['training_instructor'].choices = self.instructor_choices('instructor_id', 'name', TnrisInstructor, 'name')


class TnrisInstructorForm(forms.ModelForm):
    class Meta:
        model = TnrisInstructor
        fields = ('__all__')

    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":25, "cols":20}), help_text="Enter plain text, no html or markdown.")
    headshot = forms.URLField(required=False, widget=HeadshotWidget, help_text="Paste the S3 url for this instructor's headshot photo here. Example: 'https://tnris-org-static.s3.amazonaws.com/images/name_headshot.jpg'")
