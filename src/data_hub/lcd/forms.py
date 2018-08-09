from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from string import Template
from django.utils.safestring import mark_safe

# from django.core.exceptions import ValidationError
from django.db.utils import ProgrammingError
from .models import (Collection,
                     BandRelate,
                     BandType,
                     CategoryRelate,
                     CategoryType,
                     DataTypeRelate,
                     DataType,
                     EpsgRelate,
                     EpsgType,
                     FileTypeRelate,
                     FileType,
                     ResolutionRelate,
                     ResolutionType,
                     UseRelate,
                     UseType)

import boto3

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<input type="file" name="$name" id="id_$name"><label for="img_$name">Current: $link</label><img id="img_$name" src="$link" style="max-width:500px;"/>""")
        return mark_safe(html.substitute(link=value,name=name))

class CollectionForm(forms.ModelForm):
    # base model is Collection
    class Meta:
        model = Collection
        fields = ('__all__')

    # adjust some field types so their form inputs are pretty
    name = forms.CharField(widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=150)
    acquisition_date = forms.DateField(required=False, widget=AdminDateWidget())
    known_issues = forms.CharField(required=False, widget=forms.Textarea(), initial='None')
    carto_map_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=50)

    overview_image = forms.FileField(required=False, widget=PictureWidget)
    thumbnail_image = forms.FileField(required=False, widget=PictureWidget)
    natural_image = forms.FileField(required=False, widget=PictureWidget)
    urban_image = forms.FileField(required=False, widget=PictureWidget)

    delete_overview_image = forms.BooleanField(required=False)
    delete_thumbnail_image = forms.BooleanField(required=False)
    delete_natural_image = forms.BooleanField(required=False)
    delete_urban_image = forms.BooleanField(required=False)

    # boto3 s3 object
    client = boto3.client('s3')

    # generic function to create a form input for a relate table
    def create_relate_field(id_field, label_field, type_table, order_field):
        # get the relate type choices from the type table
        try:
            choices = (
                (getattr(b, id_field), getattr(b, label_field)) for b in type_table.objects.all().order_by(order_field))
        except ProgrammingError:
            choices = ()
        # create the input
        input = forms.MultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}),
            choices=choices
        )
        return input

    # fire function to create the relate form inputs
    bands = create_relate_field('band_type_id', 'band_name', BandType, 'band_name')
    categories = create_relate_field('category_type_id', 'category', CategoryType, 'category')
    data_types = create_relate_field('data_type_id', 'data_type', DataType, 'data_type')
    projections = create_relate_field('epsg_type_id', 'epsg_code', EpsgType, 'epsg_code')
    file_types = create_relate_field('file_type_id', 'file_type', FileType, 'file_type')
    resolutions = create_relate_field('resolution_type_id', 'resolution', ResolutionType, 'resolution')
    uses = create_relate_field('use_type_id', 'use_type', UseType, 'use_type')

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
            self.attribute_initial_values('bands', BandRelate, 'band_type_id')
            self.attribute_initial_values('categories', CategoryRelate, 'category_type_id')
            self.attribute_initial_values('data_types', DataTypeRelate, 'data_type_id')
            self.attribute_initial_values('projections', EpsgRelate, 'epsg_type_id')
            self.attribute_initial_values('file_types', FileTypeRelate, 'file_type_id')
            self.attribute_initial_values('resolutions', ResolutionRelate, 'resolution_type_id')
            self.attribute_initial_values('uses', UseRelate, 'use_type_id')

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
            collection_record = Collection.objects.get(collection_id=self.instance.collection_id)
            args = {'collection_id': collection_record}

            type_arg = {}
            type_arg[id_field] = add
            type_record = type_table.objects.get(**type_arg)
            args[id_field] = type_record

            relate_table(**args).save()
        return

    # generic function to upload image and update dbase link
    def handle_image(self, field, file):
        key = "%s/assets/%s" % (self.instance.collection_id, field.replace('_image', '.jpg'))
        response = self.client.put_object(
            Bucket='data.tnris.org',
            ACL='public-read',
            Key=key,
            Body=file
        )
        print('%s upload success!' % key)
        setattr(self.instance, field, "https://s3.amazonaws.com/data.tnris.org/" + key)
        return

    # generic function to delete images fired by check of checkboxes on adminform
    def delete_image(self, field):
        key = "%s/assets/%s" % (self.instance.collection_id, field.replace('delete_', '').replace('_image', '.jpg'))
        response = self.client.delete_object(
            Bucket='data.tnris.org',
            Key=key
        )
        print('%s delete success!' % key)
        field = field.replace('delete_', '')
        setattr(self.instance, field, None)
        return

    # custom handling of various relationships on save method
    def save(self, commit=True):
        # on save fire function to apply updates to relate tables
        self.update_relate_table('bands', BandRelate, 'band_type_id', BandType)
        self.update_relate_table('categories', CategoryRelate, 'category_type_id', CategoryType)
        self.update_relate_table('data_types', DataTypeRelate, 'data_type_id', DataType)
        self.update_relate_table('projections', EpsgRelate, 'epsg_type_id', EpsgType)
        self.update_relate_table('file_types', FileTypeRelate, 'file_type_id', FileType)
        self.update_relate_table('resolutions', ResolutionRelate, 'resolution_type_id', ResolutionType)
        self.update_relate_table('uses', UseRelate, 'use_type_id', UseType)
        # check for files
        files = self.files
        image_fields = ['overview_image', 'thumbnail_image', 'natural_image', 'urban_image']
        # if files and field not marked for deletion then upload to s3
        for f in files:
            delete_checkbox = 'delete_' + f
            if f in image_fields and self.cleaned_data[delete_checkbox] is False:
                self.handle_image(f, files[f])
        # iterate deletion checkboxes and if checked then delete associated
        # file from s3
        deletion_flags = ['delete_overview_image',
                          'delete_thumbnail_image',
                          'delete_natural_image',
                          'delete_urban_image']
        for d in deletion_flags:
            if self.cleaned_data[d] is True:
                self.delete_image(d)

        return super(CollectionForm, self).save(commit=commit)


#
# -------------------------------------
#
# EVEYTHING BELOW THIS LINE CAN BE DELETED.
# Reminents from data concierge
#
# -------------------------------------
#
#

#
#
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#     def clean(self):
#         try:
#             if (self.cleaned_data.get('number_of_frames')
#                     < self.cleaned_data.get('scanned')):
#                 raise ValidationError("Scanned must be >= number of frames")
#         except Exception:
#             raise ValidationError("Scanned must be >= number of frames")
#         return self.cleaned_data
# class CharTextInput(forms.widgets.TextInput):
#     """Subclass TextInput since there's no direct way to override its type attribute"""
#     input_type ='email'
