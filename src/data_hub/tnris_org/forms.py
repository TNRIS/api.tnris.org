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
import os, re
import boto3, uuid


# widget template overrides for populated upload file fields
def populated_image_render(name, value, attrs=None, renderer=None):
    cdn_link = value.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/')
    html = Template("""
        <div style="margin-bottom:10px;">
            <input style="width:90%;" type="text" id="currentUrl" value="$link" readonly></input>
        </div>
        <div style="margin-bottom:10px;">
            <img id="img_$name" style="max-height:500px; max-width: 95%;" src="$link"/>
        </div>
        <br>
        <p>S3 Path: $value</p>
    """)
    return mark_safe(html.substitute(value=value, link=cdn_link, name=name))

def populated_document_render(name, value, attrs=None, renderer=None):
    cdn_link = value.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/')
    html = Template("""
            <div style="margin-bottom:10px;">
                <input style="width:90%;" type="text" id="currentUrl" value="$link" readonly></input>
            </div>
            <br>
            <p>S3 Path: $value</p>
        """)
    return mark_safe(html.substitute(value=value, link=cdn_link))

def populated_headshot_render(name, value, attrs=None, renderer=None):
    cdn_link = value.replace('https://tnris-org-static.s3.amazonaws.com/', 'https://cdn.tnris.org/')
    html = Template("""
        <input type="text" name="$name" id="id_$name" style="width:758px;"></input>
        <br>
        <label for="img_$name">Current: <a href="$link" target="_blank">$link</a></label>
        <img id="img_$name" src="$link" style="max-height:250px; max-width:250px; margin:20px 20px;"/>
        <br>
        <p>S3 Path: $value</p>
    """)
    return mark_safe(html.substitute(value=value, link=cdn_link, name=name))


class ImageForm(forms.ModelForm):
    class Meta:
        model = TnrisImage
        fields = ('__all__')

    image_url = forms.FileField(
        required=False,
        help_text="Choose an image file and 'Save' this form to upload & save it to the database. To replace this image with a new one, delete the image and create a new one."
    )
    carousel = forms.BooleanField(
        required=False,
        label="Carousel Image",
        help_text="Check this box if you'd like this image to show up on the tnris.org front page image carousel."
    )
    carousel_caption = forms.CharField(
        required=False,
        label="Carousel Caption",
        max_length=200,
        widget=forms.Textarea(attrs={"rows":3, "cols":20}),
        help_text="Enter caption text for this carousel image. 200 character limit."
    )
    carousel_link = forms.URLField(
        required=False,
        label="Carousel Link",
        widget=forms.Textarea(attrs={"rows":1, "cols":20}),
        help_text="Enter a URL that you would like to send users to if they click this carousel image."
    )
    carousel_order = forms.IntegerField(
        required=False,
        label="Carousel Image Order",
        help_text="Enter a number for the order you would like this image to appear in the carousel. A number 1 will show first."
    )

    # boto3 s3 object
    client = boto3.client('s3')

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        if self.instance.image_url != '':
            self.fields['image_url'].widget.render = populated_image_render

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
            valid_extensions = ['.ico', '.jpg', '.png', '.gif', '.jpeg', '.svg']
            # validation to prevent non-standard image formats or other files from being uploaded
            if not ext.lower() in valid_extensions:
                raise ValidationError(u"Unsupported file extension. Only .ico, .jpg, .png, .gif, and .jpeg file extensions supported for Tnris Images")
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

    document_file = forms.FileField(
        required=False,
        help_text="Choose a document file and 'Save' this form to upload & save it to the database. Uploaded files cannot be overwritten; the best method to overwrite would be to delete this record (deletes the file as well) and re-upload in a new record."
    )
    sgm_note = forms.BooleanField(
        required=False,
        label="GIS Solutions Group Notes",
        help_text="Check this box to identify a GIS Solutions Group notes document.<br><br><strong>Note:</strong> This is required to view the document on the website at '/geographic-information-office/gis-solutions-group/'. Be sure to give a descriptive Document Name above."
    )
    comm_note = forms.BooleanField(
        required=False,
        label="GIS Community Meeting Notes",
        help_text="Check this box to identify a GIS Community Meeting notes document.<br><br><strong>Note:</strong> This is required to view the document on the website at '/geographic-information-office/'. Be sure to give a descriptive Document Name above."
    )

    # boto3 s3 object
    client = boto3.client('s3')

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['document_url'].help_text = "Paste the URL path to a video or file. Example: https://youtu.be/jS2-sjNixr0"
        self.fields['document_url'].required = False
        if self.instance.document_url != '':
            self.fields['document_url'].widget.render = populated_document_render
            self.fields['document_file'].widget.attrs['readonly'] = True
            self.fields['document_file'].widget.attrs['disabled'] = True

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
        setattr(self.instance, 'document_url', "https://tnris-org-static.s3.amazonaws.com/" + key)
        return

    # custom handling of documents on save
    def clean(self, commit=True):
        # if no document name, throw error early. this prevents an unwanted file upload
        if 'document_name' not in self.cleaned_data.keys():
            raise ValidationError(u"Document Name is required.")
        # validation to check if document_name already exists in database
        name_set = TnrisDocument.objects.filter(document_name=self.cleaned_data['document_name'])
        if len(name_set) > 0:
            if name_set[0].document_id != self.instance.document_id:
                raise ValidationError(u"Document Name already exists, all names must be unique. Enter a different Document Name and try again.")
        # if no url present on the instance (it's a new record if so) and no file being uploaded
        # or url entered, then throw the error as URL is required
        if (self.instance.document_url == '' and
            self.cleaned_data['document_url'] == '' and
            self.cleaned_data['document_file'] is None):
            raise ValidationError(u"A 'Document file' or 'Document URL' is required.")
        # throw error if attempting to both upload file and set a URL on new record creation
        if (self.instance.document_url == '' and
            self.cleaned_data['document_url'] != '' and
            self.cleaned_data['document_file'] is not None):
            raise ValidationError(u"Can only choose 'Document file' or 'Document URL', not both. Choose one and try again.")
        # check for files. if files present and no URL entered, then do the upload.
        # if no files, or a URL is entered, ignore the file and go with the URL. this prevents
        # the unused and untracked file from being uploaded.
        files = self.files
        if len(files) > 0 and self.cleaned_data['document_url'] == '':
            for f in files:
                ext = os.path.splitext(str(files[f]))[1]
                invalid_extensions = ['.jpg', '.png', '.gif', '.jpeg', '.svg']
                # validation to prevent image formats from being uploaded
                if ext.lower() in invalid_extensions:
                    raise ValidationError(u"Unsupported file extension. All images should be uploaded to 'Tnris Images', only document type files should be uploaded here.")
                # validation to prevent bad URL characters in filename
                regex = re.compile('[@!#$%^&*()<>?/\|}{~:,]')
                if regex.search(str(files[f])) is not None:
                    raise ValidationError(u"Bad character(s) in filename. Filename characters must be URL friendly. Exclude: [@!#$%^&*()<>?/\|}{~:,]")
                # validation to check if document_file name already exists in database (also in s3 since one-in-the-same)
                regex_str = str(files[f]) + "$"
                filename_set = TnrisDocument.objects.filter(document_url__regex=regex_str)
                if len(filename_set) > 0:
                    raise ValidationError(u"Document File name already exists, all uploaded files must be uniquely named. Rename your file and try again.")
                self.handle_doc(f, files[f])
        # if instance already had a url (updating rather than creating new), deliberately reset
        # the current document_url into the form's cleaned_data as to prevent overwriting the field
        # with an empty string from the uneditable field in the form
        if self.instance.document_url != '' and self.cleaned_data['document_url'] == '':
            self.cleaned_data['document_url'] = self.instance.document_url
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

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows":25, "cols":20}),
        help_text="Enter plain text, no html or markdown."
    )
    headshot = forms.URLField(
        required=False,
        help_text="Paste the S3 url for this instructor's headshot photo in the input above.<br><strong>Example headshot url:</strong> 'https://cdn.tnris.org/images/name_headshot.jpg'<br><strong>*NOTE:</strong> Headshot preview in this form may not reflect actual size of the image."
    )

    def __init__(self, *args, **kwargs):
        super(TnrisInstructorTypeForm, self).__init__(*args, **kwargs)
        if self.instance.headshot != '' and self.instance.headshot is not None:
            self.fields['headshot'].widget.render = populated_headshot_render

    # custom handling of documents on save
    def clean(self, commit=True):
        self.cleaned_data['headshot'] = self.cleaned_data['headshot'].replace('https://cdn.tnris.org/', 'https://tnris-org-static.s3.amazonaws.com/')
        if self.cleaned_data['headshot'] == "":
            self.cleaned_data['headshot'] = None
        super(TnrisInstructorTypeForm, self).save(commit=commit)
        return
