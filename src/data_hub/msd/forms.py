from django import forms
from django.core.exceptions import ValidationError

from string import Template
from django.utils.safestring import mark_safe

from django.db.utils import ProgrammingError
from .models import (
    MapCollection,
    MapDataRelate,
    MapDownload,
    MapSize,
    PixelsPerInch
)

import os
import boto3, json

from lcd.models import Collection


# widget template overrides for populated upload file fields
def populated_image_render(name, value, attrs=None, renderer=None):
    cdn_link = value.replace('https://s3.amazonaws.com/data.tnris.org/', 'https://data.tnris.org/')
    html = Template("""
        <div style="margin-bottom:10px;">
            <input style="width:90%;" type="text" id="currentUrl" value="$link" readonly></input>
        </div>
        <div style="margin-bottom:10px;">
            <img id="img_$name" style="max-height:500px; max-width: 95%;" src="$link"/>
        </div>
        <p>S3 Path: $value</p>
    """)
    return mark_safe(html.substitute(value=value, link=cdn_link, name=name))


def populated_pdf_render(name, value, attrs=None, renderer=None):
    cdn_link = value.replace('https://s3.amazonaws.com/data.tnris.org/', 'https://data.tnris.org/')
    js = """
    <script type="text/javascript">
        function copyFunction() {
            var copyText = document.getElementById("currentUrl");
            copyText.select();
            document.execCommand("copy");
        }
    </script>
    """
    html = Template("""
            {0}
            <div style="margin-bottom:10px;">
                <a style="cursor:pointer;border:solid 1px;padding:3px;" onclick="copyFunction();">COPY URL</a>
            </div>
            <div alt="$link" style="margin-bottom:10px;">
                <input id="currentUrl" value="$link" readonly style="width: 80%;padding:3px;cursor:default;"></input>
            </div>
            <br>
            <p>S3 Path: $value</p>

        """.format(js))
    return mark_safe(html.substitute(value=value, link=cdn_link))


class MapDownloadForm(forms.ModelForm):
    class Meta:
        model = MapDownload
        fields = (
            'map_collection_id',
            'map_size',
            'pixels_per_inch',
            'label'
            )

    download_url = forms.FileField(
        required=False,
        help_text="Upload map download file. PDF is recommended. 75MB max size. Overwriting files is not allowed. Delete the record and create a new one with the new file if you are attempting to overwrite."
    )

    def __init__(self, *args, **kwargs):
        super(MapDownloadForm, self).__init__(*args, **kwargs)
        if self.instance.download_url != '':
            self.fields['download_url'].widget.render = populated_pdf_render

    # FILE UPLOAD FOR DOWNLOAD FILE (PDF SUGGESTED)
    # boto3 s3 object
    client = boto3.client('s3')

    def handle_upload(self, file):
        # set proper content type base on file extension
        content_type = 'binary/octet-stream'
        ext = os.path.splitext(str(file))[-1]
        ext_ref = {
            '.pdf': 'application/pdf',
            '.zip': 'application/zip',
            '.jpg': 'image',
            '.png': 'image',
            '.wav': 'audio/x-wav',
            '.svg': 'image/svg+xml'
        }
        if ext.lower() in ext_ref.keys():
            content_type = ext_ref[ext.lower()]
        # upload new download file
        special_characters = [' ', '-', '(', ')']
        filename = file._name
        for sc in special_characters:
            filename = filename.replace(sc, '_')
        key = "%s/assets/%s-%s" % (self.cleaned_data['map_collection_id'].map_collection_id, self.instance.map_download_id, filename)
        response = self.client.put_object(
            Bucket='data.tnris.org',
            ACL='public-read',
            ContentType=content_type,
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)

        # update link in database table
        setattr(self.instance, 'download_url', "https://s3.amazonaws.com/data.tnris.org/" + key)
        self.cleaned_data['download_url'] = "https://s3.amazonaws.com/data.tnris.org/" + key
        return

    def clean(self):
        if len(self.files.keys()) == 0 and (self.instance.download_url == None or self.instance.download_url == ''):
            raise forms.ValidationError('You must select a file to upload for the Download Url!')
        # handle map download upload
        files = self.files
        for f in files:
            if f == 'download_url':
                self.handle_upload(files[f])
            else:
                print("where did this file come from???? shouldn't be possible.")
        return self.cleaned_data

    def save(self, commit=True):
        # fire lambda to refresh the MsdView
        client = boto3.client('lambda')
        payload = {'materialized_view': 'master_systems_display'}
        response = client.invoke(
            FunctionName='api-tnris-org-refresh_materialized_views',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        print(response)
        
        return super(MapDownloadForm, self).save(commit=commit)


class MapCollectionForm(forms.ModelForm):
    class Meta:
        model = MapCollection
        help_texts = {
            'data_collections': 'Hold down CTRL to add/remove multiple data collections.',
        }
        fields = ('name', 'publish_date', 'description', 'public',
                  'thumbnail_link', 'data_collections', 'more_info_link')

    thumbnail_link = forms.FileField(
        required=False,
        help_text=".JPG Format Only!"
    )
    delete_thumbnail = forms.BooleanField(required=False)

    # RELATED LCD DATA COLLECTIONS
    try:
        data_collection_choices = (
            (c.collection_id, str(c.acquisition_date)[:4].replace('None', '') + ' ' + c.name) for c in Collection.objects.all().order_by("name", "acquisition_date")
            )
    except Exception as e:
        print(e)
        data_collection_choices = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_data_collections = []
        if self.instance:
            self.initial_data_collections = [
                c[0] for c in MapDataRelate.objects.values_list(
                    "data_collection_id").filter(map_collection_id=self.instance.map_collection_id)
            ]
            self.fields['data_collections'].initial = self.initial_data_collections
        if self.instance.thumbnail_link != None:
            self.fields['thumbnail_link'].widget.render = populated_image_render

    data_collections = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple data collections',}),
        choices=data_collection_choices,
        required=False
    )

    # FILE UPLOAD FOR THUMBNAIL IMAGE
    # boto3 s3 object
    client = boto3.client('s3')

    def handle_thumbnail(self, field, file):
        # upload image
        key = "%s/assets/%s" % (self.instance.map_collection_id, 'thumbnail.jpg')
        response = self.client.put_object(
            Bucket='data.tnris.org',
            ACL='public-read',
            ContentType='image',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        self.cleaned_data[field] = "https://s3.amazonaws.com/data.tnris.org/" + key
        return

    # generic function to delete s3 objects fired by check of checkboxes on adminform
    def delete_thumbnail_from_s3(self, field):
        # delete from s3
        key = "%s/assets/thumbnail.jpg" % (self.instance.map_collection_id)
        response = self.client.delete_object(
            Bucket='data.tnris.org',
            Key=key
        )
        print('%s delete success!' % key)
        # clear link from database table
        self.cleaned_data[field] = None
        return

    # custom handling of thumbnail image on save
    def clean(self):
        # check for files
        files = self.files
        for f in files:
            ext = os.path.splitext(str(files[f]))[1]
            # validation to prevent non-jpg image format from being uploaded
            if ext.lower() != '.jpg':
                raise ValidationError(u"Unsupported thumbnail file extension. Only .jpg format permitted!")
            if f == 'thumbnail_link' and self.cleaned_data['delete_thumbnail'] is False:
                self.handle_thumbnail(f, files[f])
        # handle s3 deletions
        if self.cleaned_data['delete_thumbnail'] is True:
            self.delete_thumbnail_from_s3('thumbnail_link')
        if 'name' not in self.cleaned_data.keys():
            raise forms.ValidationError('"Name" field is required.')
        if 'publish_date' not in self.cleaned_data.keys():
            raise forms.ValidationError('"Publish Date" field is required.')
        super(MapCollectionForm, self).save(commit=False)
        return

    def save(self, commit=True):
        # update lcd data collection relate records
        updated_data_collections = self.cleaned_data['data_collections']
        initial_data_collections_str = [
            str(u) for u in self.initial_data_collections
        ]
        removes = [c for c in initial_data_collections_str if c not in updated_data_collections]
        adds = [c for c in updated_data_collections if c not in initial_data_collections_str]
        for remove in removes:
            MapDataRelate.objects.filter(
                data_collection_id=remove).filter(map_collection_id=self.instance).delete()
        for add in adds:
            data_collection_rec = Collection.objects.get(collection_id=add)
            MapDataRelate(data_collection_id=data_collection_rec, map_collection_id=self.instance).save()

        # fire lambda to refresh the MsdView
        client = boto3.client('lambda')
        payload = {'materialized_view': 'master_systems_display'}
        response = client.invoke(
            FunctionName='api-tnris-org-refresh_materialized_views',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        print(response)

        return super(MapCollectionForm, self).save(commit=commit)
