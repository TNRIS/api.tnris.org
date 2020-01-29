from django import forms
from django.core.exceptions import ValidationError
# from django.db.utils import ProgrammingError

from .models import MapCollection, MapDataRelate, MapDownload, MapSize, PixelsPerInch
from lcd.models import Collection

from string import Template
from django.utils.safestring import mark_safe

import boto3, os


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<input type="file" name="$name" id="id_$name"><label for="img_$name" style='font-weight:bold;'>Current: $link</label><img id="img_$name" src="$link" style="max-width:500px;"/>""")
        return mark_safe(html.substitute(link=value,name=name))


class PdfWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        if value:
            html = Template("""<label for="img_$name" style='font-weight:bold;'>Current: $link</label>""")
        else:
            html = Template("""<input type="file" name="$name" id="id_$name"></input>""")
        return mark_safe(html.substitute(link=value,name=name))


class MapDownloadForm(forms.ModelForm):
    class Meta:
        model = MapDownload
        fields = (
            'map_collection_id',
            'map_size',
            'pixels_per_inch',
            'label'
            )

    download_url = forms.FileField(required=False, widget=PdfWidget, help_text="Upload map download file. PDF is recommended. 75MB max size. Overwriting files is not allowed. Delete the record and create a new one with the new file if you are attempting to overwrite.")

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
        # if replacing a download file, delete the old one
        if self.instance.download_url is not None and self.cleaned_data['download_url'] is not None:
            old_key = self.cleaned_data['download_url'].replace('https://s3.amazonaws.com/data.tnris.org/', '')
            response = self.client.delete_object(
                Bucket='data.tnris.org',
                Key=old_key
            )
            print('deleted: ' + old_key)

        # update link in database table
        setattr(self.instance, 'download_url', "https://s3.amazonaws.com/data.tnris.org/" + key)
        self.cleaned_data['download_url'] = "https://s3.amazonaws.com/data.tnris.org/" + key
        return

    def clean(self):
        if len(self.files.keys()) == 0 and (self.instance.download_url == None or self.instance.download_url == ''):
            raise forms.ValidationError('You must select a file to upload for the Download Url!')
        return self.cleaned_data

    def save(self, commit=True):
        # handle map download upload
        files = self.files
        for f in files:
            if f == 'download_url':
                self.handle_upload(files[f])
            else:
                print("where did this file come from???? shouldn't be possible.")
        return super(MapDownloadForm, self).save(commit=commit)


class MapCollectionForm(forms.ModelForm):
    class Meta:
        model = MapCollection
        help_texts = {
            'data_collections': 'Hold down CTRL to add/remove multiple data collections.',
        }
        fields = ('name', 'publish_date', 'description', 'public',
                  'thumbnail_link', 'data_collections', 'more_info_link')

    thumbnail_link = forms.FileField(required=False, widget=PictureWidget, help_text=".JPG Format Only!")
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
    def clean(self, commit=True):
        # check for files
        files = self.files
        for f in files:
            print(str(files[f]))
            ext = os.path.splitext(str(files[f]))[1]
            # validation to prevent non-jpg image format from being uploaded
            if ext.lower() != '.jpg':
                raise ValidationError(u"Unsupported thumbnail file extension. Only .jpg format permitted!")
            if f == 'thumbnail_link' and self.cleaned_data['delete_thumbnail'] is False:
                self.handle_thumbnail(f, files[f])
        # handle s3 deletions
        if self.cleaned_data['delete_thumbnail'] is True:
            self.delete_thumbnail_from_s3('thumbnail_link')
        super(MapCollectionForm, self).save(commit=commit)
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
        return super(MapCollectionForm, self).save(commit=commit)
