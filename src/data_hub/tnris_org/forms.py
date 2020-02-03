from django import forms
from django.core.exceptions import ValidationError

from string import Template
from django.utils.safestring import mark_safe

from django.db.utils import ProgrammingError
from .models import (
    TnrisImage,
    TnrisDocument,
    TnrisTraining,
    TnrisForumTraining,
    TnrisInstructorType,
    TnrisInstructorRelate
)
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
            html = Template("""{0}<div style="margin-bottom:10px;"><a style="cursor:pointer;border:solid 1px;padding:3px;" onclick="copyFunction();">COPY URL</a></div><div style="margin-bottom:10px;"><input style="width:50%;" type="text" id="currentUrl" value="$link" readonly></input></div><div style="margin-bottom:10px;"><img id="img_$name" src="$link"/></div>""".format(js))
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
            html = Template("""{0}<div style="margin-bottom:10px;"><a style="cursor:pointer;border:solid 1px;padding:3px;" onclick="copyFunction();">COPY URL</a></div><div style="margin-bottom:10px;"><input style="width:50%;" type="text" id="currentUrl" value="$link" readonly></input></div>""".format(js))
        return mark_safe(html.substitute(link=value,name=name))


class HeadshotWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            html = Template("""<input type="text" name="$name" id="id_$name" style="width:758px;"></input>""")
        else:
            html = Template("""<input type="text" name="$name" id="id_$name" style="width:758px;"></input><br><label for="img_$name">Current: <a href="$link" target="_blank">$link</a></label><img id="img_$name" src="$link" style="max-height:250px; max-width:250px; margin:20px 20px;"/>""")
        return mark_safe(html.substitute(link=value,name=name))


class ImageForm(forms.ModelForm):
    class Meta:
        model = TnrisImage
        fields = ('__all__')

    image_url = forms.FileField(required=False, widget=PictureWidget, help_text="Choose an image file and 'Save' this form to upload & save it to the database. Attempting to overwrite with a new file will only create a new record. The best method to overwrite would be to delete the existing file and re-upload a new file with the same name.")

    # boto3 s3 object
    client = boto3.client('s3')

    # function to upload image to s3 and update dbase link
    def handle_image(self, field, file):
        # set proper content type base on file extension
        content_type = 'image'
        ext = os.path.splitext(str(file))[-1]
        ext_ref = {
            '.svg': 'image/svg+xml'
        }
        if ext.lower() in ext_ref.keys():
            content_type = ext_ref[ext.lower()]
        # upload image
        key = "images/%s" % (file)
        response = self.client.put_object(
            Bucket='tnris-org-static',
            ACL='public-read',
            ContentType=content_type,
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

    document_url = forms.FileField(required=False, widget=DocumentWidget, help_text="Choose a document file and 'Save' this form to upload & save it to the database. Attempting to overwrite with a new file will only create a new record. The best method to overwrite would be to delete the existing file and re-upload a new file with the same name.")
    sgm_note = forms.BooleanField(required=False, label="GIS Solutions Group Notes", help_text="Check this box to identify as a GIS Solutions Group notes document.<br><br><strong>Note:</strong> This is required to view the document on tnris.org. Be sure to name the file correctly - 'YYYY-MM-DD-GIS-SG-Meeting-Notes.pdf'. The file name is important for the order these documents are presented on tnris.org.")

    # boto3 s3 object
    client = boto3.client('s3')

    # function to upload document to s3 and update dbase link
    def handle_doc(self, field, file):
        # set proper content type base on file extension
        content_type = 'binary/octet-stream'
        ext = os.path.splitext(str(file))[-1]
        ext_ref = {
            '.pdf': 'application/pdf',
            '.zip': 'application/zip',
            '.jpg': 'image',
            '.png': 'image',
            '.wav': 'audio/x-wav'
        }
        if ext.lower() in ext_ref.keys():
            content_type = ext_ref[ext.lower()]
        # upload image
        key = "documents/%s" % (file)
        response = self.client.put_object(
            Bucket='tnris-org-static',
            ACL='public-read',
            ContentType=content_type,
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        setattr(self.instance, field, "https://tnris-org-static.s3.amazonaws.com/" + key)
        setattr(self.instance, "document_name", str(file))
        # special handling to capture boolean input value of sgm_note and save it on initial creation
        if self.cleaned_data['sgm_note'] == True:
            setattr(self.instance, "sgm_note", True)
            self.cleaned_data = self.instance.__dict__
        else:
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

    cost = forms.DecimalField(help_text="Example of accepted formats for training cost: '50.00', '999', '99.99'. Max of 6 digits and 2 decimal places.")
    registration_open = forms.BooleanField(required=False, help_text="Check the box to change registration to open. Default is unchecked.")
    public = forms.BooleanField(required=False, help_text="Check the box to make this training record visible on the website. Default is unchecked.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['start_date_time'].help_text = mark_safe("Accepted date formats: '10/25/06', '10/25/2006', '2006-10-25'.<br>Accepted time formats: '13:30' (military hour & minute), '02:00 PM' (12 hour clock & minute with AM/PM)")
            self.fields['end_date_time'].help_text = mark_safe("Accepted date formats: '10/25/06', '10/25/2006', '2006-10-25'.<br>Accepted time formats: '13:30' (military hour & minute), '02:00 PM' (12 hour clock & minute with AM/PM)")


class TnrisForumTrainingForm(forms.ModelForm):
    class Meta:
        model = TnrisForumTraining
        fields = ('__all__')

    instructors = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple instructors',}), choices=[], help_text="Select all instructors that will be participating in the training. To select more than one Instructor, hold Ctrl and click the name(s).")
    cost = forms.DecimalField(help_text="Example of accepted formats for training cost: '50.00', '999', '99.99'. Max of 6 digits and 2 decimal places.")
    registration_open = forms.BooleanField(required=False, help_text="Check the box to change registration to open. Default is unchecked.")
    public = forms.BooleanField(required=False, help_text="Check the box to make this training record visible on the website. Default is unchecked.")
    max_students = forms.IntegerField(required=False, help_text="Enter max number of students for class room.")


    # general function to create a form dropdown for instructors
    def instructor_choices(self, id_field, label_field, type_table, order_field):
        # get the relate type choices from the type table
        try:
            choices = (
                (getattr(b, id_field), getattr(b, label_field)) for b in type_table.objects.all().order_by(order_field))
        except ProgrammingError:
            choices = ()
        return choices

    # generic function to retrieve the initial relate values from the relate table
    def attribute_initial_values(self, name, relate_table, id_field):
        # attribute initial values to self as list object
        attr_name = 'initial_' + name
        setattr(self, attr_name, [])
        # get records from relate table and update initial values list
        setattr(self, attr_name, [
            b[0] for b in relate_table.objects.values_list(id_field).filter(training_relate_id=self.instance.training_id)
        ])
        self.fields[name].initial = getattr(self, attr_name)
        return

    # on instance construction fire functions to retrieve initial values
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['instructors'].choices = self.instructor_choices('instructor_type_id', 'name', TnrisInstructorType, 'name')
            self.attribute_initial_values('instructors', TnrisInstructorRelate, 'instructor_relate_id')
            self.fields['start_date_time'].help_text = mark_safe("Accepted date formats: '10/25/06', '10/25/2006', '2006-10-25'.<br>Accepted time formats: '13:30' (military hour & minute), '02:00 PM' (12 hour clock & minute with AM/PM)")
            self.fields['end_date_time'].help_text = mark_safe("Accepted date formats: '10/25/06', '10/25/2006', '2006-10-25'.<br>Accepted time formats: '13:30' (military hour & minute), '02:00 PM' (12 hour clock & minute with AM/PM)")


    # generic function to update relate table with form input changes
    def update_relate_table(self, name, relate_table, relate_field, id_field, type_table):
        attr_name = 'initial_' + name
        # get selected relate values from form input
        updated = self.cleaned_data[name]
        print(updated)
        # create list of strings of initial values for comparison
        initial_str = [
            str(u) for u in getattr(self, attr_name)
        ]
        # create lists of differences: removed relates and new added relates
        removes = [b for b in initial_str if b not in updated]
        adds = [b for b in updated if b not in initial_str]
        print(adds, removes)
        # delete removals from relate table
        for remove in removes:
            args = {}
            args[relate_field] = remove
            relate_table.objects.filter(
                **args).filter(training_relate_id=self.instance.training_id).delete()
        # create adds in relate table
        for add in adds:
            training_record = super(TnrisForumTrainingForm, self).save(commit=False)
            args = {'training_relate_id': training_record}
            print(args)
            type_arg = {}
            type_arg[id_field] = add
            type_record = type_table.objects.get(**type_arg)
            args[relate_field] = type_record

            relate_table(**args).save()
        return

    # custom handling of various relationships on save method
    def save(self, commit=True):
        # on save fire function to apply updates to relate tables
        self.update_relate_table('instructors', TnrisInstructorRelate, 'instructor_relate_id', 'instructor_type_id', TnrisInstructorType)

        return super(TnrisForumTrainingForm, self).save(commit=commit)


class TnrisInstructorTypeForm(forms.ModelForm):
    class Meta:
        model = TnrisInstructorType
        fields = ('__all__')

    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":25, "cols":20}), help_text="Enter plain text, no html or markdown.")
    headshot = forms.URLField(required=False, widget=HeadshotWidget, help_text="Paste the S3 url for this instructor's headshot photo in the input above.<br><strong>Example headshot url:</strong> 'https://tnris-org-static.s3.amazonaws.com/images/name_headshot.jpg'<br><strong>*NOTE:</strong> Headshot preview in this form may not reflect actual size of the image.")
