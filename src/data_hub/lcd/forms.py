from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget

from string import Template
from django.utils.safestring import mark_safe

from django.db.utils import ProgrammingError
from .models import (Collection,
                     AreaType,
                     CategoryRelate,
                     CategoryType,
                     CountyRelate,
                     EpsgRelate,
                     EpsgType,
                     FileTypeRelate,
                     FileType,
                     Image,
                     ResolutionRelate,
                     ResolutionType,
                     Resource,
                     ResourceType,
                     ResourceTypeRelate,
                     UseRelate,
                     UseType,
                     XlargeSupplemental)
import os, json
import boto3, botocore, uuid

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):

        if value is None:
            html = Template("""
                <input type="file" name="$name" id="id_$name"></input>
            """)
        else:
            html = Template("""
                <div style="margin-bottom:10px;">
                    <input style="width:90%;" type="text" id="currentUrl" value="$link" readonly></input>
                </div>
                <div style="margin-bottom:10px;">
                    <img id="img_$name" src="$link" style="max-height:500px; max-width:95%;"/>
                </div>
            """)
        return mark_safe(html.substitute(link=value,name=name))

class ZipfileWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = Template("""
            <input type="file" name="$name" id="id_$name"><label for="img_$name">Current: $link</label>
        """)
        return mark_safe(html.substitute(link=value,name=name))

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('__all__')
        help_texts = {
            'caption': 'Caption will not be saved until chosen image is uploaded and saved to database.',
        }

    image_url = forms.FileField(
        required=True,
        widget=PictureWidget, 
        help_text="DataHub Images should be 16:9 ratio (1920 x 1080 pixels).<br/>Choose an image file and 'Save' this form to upload & save it to the database. After saving, you can populate a Caption and re-save to apply."
        )


class CollectionForm(forms.ModelForm):
    # base model is Collection
    class Meta:
        model = Collection
        fields = ('__all__')

    # adjust some field types so their form inputs are pretty
    name = forms.CharField(widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=150, help_text="Create a concise name not redundant to metadata. Do not include a year or date. The year will be auto-appended in the frontend.")
    acquisition_date = forms.DateField(required=False, widget=AdminDateWidget(), help_text="Last date of the data acquisition. Format: YYYY-MM-DD")
    publication_date = forms.DateField(required=False, widget=AdminDateWidget(), help_text="Date TNRIS published collection to the public. Format: YYYY-MM-DD")
    known_issues = forms.CharField(required=False, widget=forms.Textarea(), initial='None')
    carto_map_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=50)

    overview_image = forms.FileField(required=False, widget=PictureWidget)
    # thumbnail_image = forms.FileField(required=False, widget=PictureWidget)
    natural_image = forms.FileField(required=False, widget=PictureWidget)
    urban_image = forms.FileField(required=False, widget=PictureWidget)

    delete_overview_image = forms.BooleanField(required=False)
    delete_thumbnail_image = forms.BooleanField(required=False)
    delete_natural_image = forms.BooleanField(required=False)
    delete_urban_image = forms.BooleanField(required=False)

    supplemental_report_url = forms.FileField(required=False, widget=ZipfileWidget, help_text="Maximum filesize 75MB")
    lidar_breaklines_url = forms.FileField(required=False, widget=ZipfileWidget, help_text="Maximum filesize 75MB")
    lidar_buildings_url = forms.FileField(required=False, widget=ZipfileWidget, help_text="Maximum filesize 75MB")
    tile_index_url = forms.FileField(required=False, widget=ZipfileWidget, help_text="Maximum filesize 75MB")

    delete_supplemental_report_url = forms.BooleanField(required=False)
    delete_lidar_breaklines_url = forms.BooleanField(required=False)
    delete_lidar_buildings_url = forms.BooleanField(required=False)
    delete_tile_index_url = forms.BooleanField(required=False)

    # boto3 s3 object
    client = boto3.client('s3')

    # generic function to create a form input for a relate table
    def create_relate_field(self, id_field, label_field, type_table, order_field):
        # get the relate type choices from the type table
        try:
            choices = (
                (getattr(b, id_field), getattr(b, label_field)) for b in type_table.objects.all().order_by(order_field))
        except ProgrammingError:
            choices = ()
        return choices

    # function to create a form input for related counties
    def create_county_choices(self, id_field, label_field, type_table, order_field):
        # get the relate type choices from the area_type table
        try:
            choices = (
                (getattr(b, id_field), getattr(b, label_field)) for b in type_table.objects.filter(area_type='county').order_by(order_field))
        except ProgrammingError:
            choices = ()
        return choices

    # general function to create a form dropdown for thumbnail image
    def create_image_choices(self, id_field, label_field, type_table, order_field):
        # get the relate type choices from the type table
        try:
            choices = (
                (getattr(b, id_field), getattr(b, label_field)) for b in type_table.objects.filter(collection_id=self.instance.collection_id).order_by(order_field))
        except ProgrammingError:
            choices = ()
        return choices

    # retrieve selected thumbnail id for helper text to display
    def selected_thumbnail(self):
        text = "NO THUMBNAIL SELECTED! Please choose an image UUID from the dropdown and 'Save' the form."
        if self.instance.thumbnail_image is not None and self.instance.thumbnail_image != "":
            text = "Currently Selected: " + self.instance.thumbnail_image.split("/")[-1]
        return text

    # fire function to create the relate form inputs
    categories = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}), choices=[], help_text="Select all categories related to this collection.")
    projections = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}), choices=[])
    file_types = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}), choices=[])
    resolutions = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}), choices=[])
    uses = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}), choices=[])
    counties = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}), choices=[], help_text="Select all counties related to this collection spatially or by metadata.")
    thumbnail_image = forms.ChoiceField(required=False, choices=[])

    # generic function to retrieve the initial relate values from the relate table
    def attribute_initial_values(self, name, relate_table, id_field):
        # attribute initial values to self as list object
        attr_name = 'initial_' + name
        setattr(self, attr_name, [])
        # get records from relate table and update initial values list
        setattr(self, attr_name, [
            b[0] for b in relate_table.objects.values_list(id_field).filter(collection_id=self.instance.collection_id)
        ])
        self.fields[name].initial = getattr(self, attr_name)
        return

    # on instance construction fire functions to retrieve initial values
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['categories'].choices = self.create_relate_field('category_type_id', 'category', CategoryType, 'category')
            self.fields['projections'].choices = self.create_relate_field('epsg_type_id', 'epsg_code', EpsgType, 'epsg_code')
            self.fields['file_types'].choices = self.create_relate_field('file_type_id', 'file_type', FileType, 'file_type')
            self.fields['resolutions'].choices = self.create_relate_field('resolution_type_id', 'resolution', ResolutionType, 'resolution')
            self.fields['uses'].choices = self.create_relate_field('use_type_id', 'use_type', UseType, 'use_type')
            self.fields['counties'].choices = self.create_county_choices('area_type_id', 'area_type_name', AreaType, 'area_type_name')
            self.fields['thumbnail_image'].choices = self.create_image_choices('image_url', 'image_id', Image, 'image_id')
            self.fields['thumbnail_image'].help_text = self.selected_thumbnail()
            self.fields['description'].help_text = "Provide as much descriptive and historical detail about this data as possible. Frontend search functionality utilizes this field to return this collection as a search result."
            if 'public' in self.fields:
                self.fields['public'].help_text = "Check the 'Public' checkbox to make this collection publically available within the live, production frontend: data.tnris.org"
            self.fields['esri_open_data_id'].help_text = "ArcGIS Online Open Data Portal 'Group ID'. This is ONLY used by 'outside-entity' template collections for injecting a list of available services directly within the collection 'Description'."
            self.fields['source_type_id'].help_text = "Choose the organization which this collection is owned by/sourced from."
            self.fields['partners'].help_text = "List all organizations/companies associated with the creation, execution, or funding of this collection."
            self.fields['popup_link'].help_text = "Link to preview the WMS service link above. For ArcServer WMS links, this is the WMS link with '?f=jsapi' replacing '/WMSServer' at the end."
            self.attribute_initial_values('categories', CategoryRelate, 'category_type_id')
            self.attribute_initial_values('projections', EpsgRelate, 'epsg_type_id')
            self.attribute_initial_values('file_types', FileTypeRelate, 'file_type_id')
            self.attribute_initial_values('resolutions', ResolutionRelate, 'resolution_type_id')
            self.attribute_initial_values('uses', UseRelate, 'use_type_id')
            self.attribute_initial_values('counties', CountyRelate, 'area_type_id')
            # set aside name so we can monitor if it was edited when save() fires
            self.og_name = self.instance.name

    # generic function to update relate table with form input changes
    def update_relate_table(self, name, relate_table, id_field, type_table):
        attr_name = 'initial_' + name
        # get selected relate values from form input
        updated = self.cleaned_data[name]
        # create list of strings of initial values for comparison
        initial_str = [
            str(u) for u in getattr(self, attr_name)
        ]
        # create lists of differences: removed relates and new added relates
        removes = [b for b in initial_str if b not in updated]
        adds = [b for b in updated if b not in initial_str]
        # delete removals from relate table
        for remove in removes:
            args = {}
            args[id_field] = remove
            relate_table.objects.filter(
                **args).filter(collection_id=self.instance.collection_id).delete()
        # create adds in relate table
        for add in adds:
            collection_record = super(CollectionForm, self).save(commit=False)
            args = {'collection_id': collection_record}
            type_arg = {}
            type_arg[id_field] = add
            type_record = type_table.objects.get(**type_arg)
            args[id_field] = type_record

            relate_table(**args).save()
        return

    # generic function to upload image and update dbase link
    def handle_image(self, field, file):
        # upload image
        key = "%s/assets/%s" % (self.instance.collection_id, field.replace('_image', '.jpg'))
        response = self.client.put_object(
            Bucket='data.tnris.org',
            ACL='public-read',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        setattr(self.instance, field, "https://s3.amazonaws.com/data.tnris.org/" + key)
        return

    def inline_image_handler(self, file):
        new_uuid = uuid.uuid4()
        file_ext = str(file).split('.')[-1]
        # upload image
        key = "%s/assets/%s.%s" % (self.instance.collection_id, new_uuid, file_ext)
        # print(key + file_ext)
        response = self.client.put_object(
            Bucket='data.tnris.org',
            ACL='public-read',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        args = {
            'image_id': new_uuid,
            'image_url': "https://s3.amazonaws.com/data.tnris.org/" + key,
            'collection_id': self.instance
        }
        Image(**args).save()
        return

    # generic function to upload zipfile and update dbase link
    def handle_zipfile(self, field, file):
        # format filename
        urlized_nm = self.instance.name.lower().replace(', ', '-').replace(' & ', '-').replace(' ', '-').replace('(', '').replace(')', '').replace('\\', '-').replace('/', '-').replace('&', '').replace(',', '-')
        sfx = '-' + field.lower().replace('_url', '.zip').replace('_', '-')
        upload_nm = urlized_nm + sfx
        # upload zipfile
        key = "%s/assets/%s" % (self.instance.collection_id, upload_nm)
        response = self.client.put_object(
            Bucket='data.tnris.org',
            ACL='public-read',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        # update link in database table
        setattr(self.instance, field, "https://s3.amazonaws.com/data.tnris.org/" + key)
        return

    # generic function to delete s3 objects fired by check of checkboxes on adminform
    def delete_from_s3(self, field):
        # format for filename
        delete_field = field.replace('delete_', '')
        if '_image' in delete_field:
            delete_field = delete_field.replace('_image', '.jpg')
        elif '_url' in delete_field:
            urlized_nm = self.instance.name.lower().replace(', ', '-').replace(' & ', '-').replace(' ', '-').replace('(', '').replace(')', '').replace('\\', '-').replace('/', '-').replace('&', '').replace(',', '-')
            delete_field = urlized_nm + '-' + delete_field.replace('_url', '.zip').replace('_', '-')
        else:
            print('Not an image or zipfile url? Where did this field come from?', field)
        # delete from s3
        key = "%s/assets/%s" % (self.instance.collection_id, delete_field)
        response = self.client.delete_object(
            Bucket='data.tnris.org',
            Key=key
        )
        print('%s delete success!' % key)
        # clear link from database table
        field = field.replace('delete_', '')
        setattr(self.instance, field, None)
        return

    # generic function to rename s3 zipfiles
    def update_s3_names(self, og_name):
        # compile all the keys
        name_map = {}
        old_key_list = []
        new_key_field = {}
        z_files = [('-supplemental-report.zip', 'supplemental_report_url'),
                   ('-lidar-breaklines.zip', 'lidar_breaklines_url'),
                   ('-lidar-buildings.zip', 'lidar_buildings_url'),
                   ('-tile-index.zip', 'tile_index_url')]
        urlized_og_nm = og_name.lower().replace(', ', '-').replace(' & ', '-').replace(' ', '-').replace('(', '').replace(')', '').replace('\\', '-').replace('/', '-').replace('&', '').replace(',', '-')
        urlized_new_nm = self.cleaned_data['name'].lower().replace(', ', '-').replace(' & ', '-').replace(' ', '-').replace('(', '').replace(')', '').replace('\\', '-').replace('/', '-').replace('&', '').replace(',', '-')
        for f in z_files:
            # compile name_map
            old = urlized_og_nm + f[0]
            new = urlized_new_nm + f[0]
            old_key = "data.tnris.org/%s/assets/%s" % (self.instance.collection_id, old)
            new_key = "%s/assets/%s" % (self.instance.collection_id, new)
            name_map[old_key] = new_key
            # set aside old key objects for deletion after copy
            no_bucket_key = "%s/assets/%s" % (self.instance.collection_id, old)
            old_key_list.append({'Key':no_bucket_key})
            # set aside new key/field map
            new_key_field[new_key] = f[1]
        # iterate keys to perform copy of old files to new filename
        for o in name_map:
            try:
                response = self.client.copy_object(
                    ACL='public-read',
                    Bucket='data.tnris.org',
                    CopySource=o,
                    Key=name_map[o]
                )
                # if copy successful then old file existed so we need to update
                # the link in the database table
                new_link = "https://s3.amazonaws.com/data.tnris.org/" + name_map[o]
                setattr(self.instance, new_key_field[name_map[o]], new_link)
            except Exception as e:
                print("copy whoopsie! (link probably doesn't exist)")
                print(e)
        # delete old keys since copies are done
        response = self.client.delete_objects(
            Bucket='data.tnris.org',
            Delete={'Objects': old_key_list}
        )
        return

    # custom handling of various relationships on save method
    def save(self, commit=True):
        # on save fire function to apply updates to relate tables
        self.update_relate_table('categories', CategoryRelate, 'category_type_id', CategoryType)
        self.update_relate_table('projections', EpsgRelate, 'epsg_type_id', EpsgType)
        self.update_relate_table('file_types', FileTypeRelate, 'file_type_id', FileType)
        self.update_relate_table('resolutions', ResolutionRelate, 'resolution_type_id', ResolutionType)
        self.update_relate_table('uses', UseRelate, 'use_type_id', UseType)
        self.update_relate_table('counties', CountyRelate, 'area_type_id', AreaType)
        # check for files
        files = self.files
        image_fields = ['overview_image', 'thumbnail_image', 'natural_image', 'urban_image']
        zipfile_fields = ['supplemental_report_url', 'lidar_breaklines_url', 'lidar_buildings_url', 'tile_index_url']
        # if files and field not marked for deletion then upload to s3
        for f in files:
            delete_checkbox = 'delete_' + f
            if f in image_fields and self.cleaned_data[delete_checkbox] is False:
                self.handle_image(f, files[f])
            elif f in zipfile_fields and self.cleaned_data[delete_checkbox] is False:
                self.handle_zipfile(f, files[f])
            elif 'image_collections' in f:
                self.inline_image_handler(files[f])
            else:
                print('New file uploaded but delete checkbox says "no!":', f)
        # iterate deletion checkboxes and if checked then delete associated
        # file from s3
        deletion_flags = ['delete_overview_image',
                          'delete_thumbnail_image',
                          'delete_natural_image',
                          'delete_urban_image',
                          'delete_supplemental_report_url',
                          'delete_lidar_breaklines_url',
                          'delete_lidar_buildings_url',
                          'delete_tile_index_url']
        for d in deletion_flags:
            if self.cleaned_data[d] is True:
                self.delete_from_s3(d)
        # detect name update and fix s3 zipfile keys
        if self.og_name != self.instance.name and self.og_name is not None:
            self.update_s3_names(self.og_name)

        return super(CollectionForm, self).save(commit=commit)


class ResourceForm(forms.ModelForm):
    # base model is Collection
    class Meta:
        model = Resource
        fields = ('__all__')

    # boto3 s3 object
    client = boto3.client('s3')

    # specific function to create the Collection field dropdown
    def create_collection_field(self):
        # get the Collection choices from the Collection table
        try:
            choices = []
            for b in Collection.objects.all().order_by('name'):
                if b.acquisition_date is not None and b.template_type_id.template != 'outside-entity':
                    year = b.acquisition_date.split("-")[0] + " "
                else:
                    year = ""
                disp_name = year + b.name
                choices.append((b.collection_id, disp_name))

        except ProgrammingError:
            choices = ()
        # return the choices
        return choices

    # create collection dropdown with empty choices as placeholder
    collection = forms.ChoiceField(required=True, label="Collection", choices=[])

    # on instance construction fire functions to retrieve initial/dropdown values
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.created is None:
            # fire function to create the Collection field dropdown
            self.fields['collection'].choices = self.create_collection_field()

    # invoke lambda to perform database update. no actual records saved here in admin console
    def clean(self):
        try:
            print('invoking app-resource-update')
            client = boto3.client('lambda')
            payload = {'collection_id': self.cleaned_data['collection']}
            response = client.invoke(
                FunctionName='api-resource-update',
                InvocationType='Event',
                Payload=json.dumps(payload)
            )
            print(response)
            if response['StatusCode'] != 202:
                raise forms.ValidationError('Response error when invoking "api-resource-update" lambda. Response code: %s' % (str(response['StatusCode'])))
        except Exception as e:
            print(e)
            raise forms.ValidationError('Local error invoking "api-resource-update" lambda. Please contact the IS team for assistance.')
        super(ResourceForm, self).save(commit=False)
        return


class XlargeSupplementalForm(forms.ModelForm):
    class Meta:
        model = XlargeSupplemental
        fields = ('__all__')

    # boto3 s3 object
    s3 = boto3.resource('s3')

    # specific function to create the Collection field dropdown
    def create_collection_field(self):
        # get the Collection choices from the Collection table
        try:
            choices = []
            for b in Collection.objects.all().order_by('name'):
                if b.acquisition_date is not None and b.template_type_id.template != 'outside-entity':
                    year = b.acquisition_date.split("-")[0] + " "
                else:
                    year = ""
                disp_name = year + b.name
                choices.append((b.collection_id, disp_name))

        except ProgrammingError:
            choices = ()
        # return the choices
        return choices

    # create collection dropdown with empty choices as placeholder
    collection = forms.ChoiceField(required=True, label="Collection", choices=[])

    supplemental_choices = [
        ('lidar_breaklines_url', 'Lidar Breaklines'),
        ('lidar_buildings_url', 'Lidar Buildings'),
        ('supplemental_report_url', 'Supplemental Report'),
        ('tile_index_url', 'Tile Index')
    ]
    supplemental_type = forms.ChoiceField(required=True, label="Supplemental Type", choices=[])

    # on instance construction fire functions to retrieve initial/dropdown values
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fire function to create the Collection field dropdown
        self.fields['collection'].choices = self.create_collection_field()
        self.fields['supplemental_type'].choices = self.supplemental_choices

    # generic function to retrieve the associated Collection object
    def get_collection_obj(self, collection_id):
        record = Collection.objects.get(collection_id=collection_id)
        return record

    # generic function to verify zipfile exists in s3 with proper key
    def verify_s3_zipfile(self, key):
        try:
            self.s3.Object('data.tnris.org', key).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise forms.ValidationError('Zipfile not in s3! Could not find the data.tnris.org bucket key: %s' % (key))
            else:
                raise forms.ValidationError('Error verifying zipfile in s3. Try again or contact IS team.')
        else:
            print('s3 zipfile found.')
            return

    # custom handling in save method for adding multiple new records
    def clean(self):
        # get the collection
        try:
            collection_obj = self.get_collection_obj(self.cleaned_data['collection'])
        except:
            raise forms.ValidationError('Could not retrieve "%s" from the collection table. This is extremely peculiar... What did you do???' % (self.cleaned_data['collection']))
        # format filename
        urlized_nm = collection_obj.name.lower().replace(', ', '-').replace(' & ', '-').replace(' ', '-').replace('(', '').replace(')', '').replace('\\', '-').replace('/', '-').replace('&', '').replace(',', '-')
        supp_field = self.cleaned_data['supplemental_type']
        sfx = '-' + supp_field.lower().replace('_url', '.zip').replace('_', '-')
        upload_nm = urlized_nm + sfx
        # uploaded zipfile url
        key = "%s/assets/%s" % (collection_obj.collection_id, upload_nm)
        url = "https://s3.amazonaws.com/data.tnris.org/%s" % (key)
        # verify the file has been uploaded to s3
        self.verify_s3_zipfile(key)
        # verified! make the dbase update
        print("updating %s collection's %s field with value %s" % (collection_obj.collection_id, supp_field, url))
        setattr(collection_obj, supp_field, url)
        collection_obj.save()
        self.instance.key = key
        return
