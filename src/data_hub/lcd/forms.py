from django import forms
from django.contrib.admin.widgets import AdminDateWidget

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

    overview_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}), initial='images/placeholder.png')
    thumbnail_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}), initial='images/placeholder.png')
    natural_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}))
    urban_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}))

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

    # on save fire function to apply updates to relate tables
    def save(self, commit=True):
        self.update_relate_table('bands', BandRelate, 'band_type_id', BandType)
        self.update_relate_table('categories', CategoryRelate, 'category_type_id', CategoryType)
        self.update_relate_table('data_types', DataTypeRelate, 'data_type_id', DataType)
        self.update_relate_table('projections', EpsgRelate, 'epsg_type_id', EpsgType)
        self.update_relate_table('file_types', FileTypeRelate, 'file_type_id', FileType)
        self.update_relate_table('resolutions', ResolutionRelate, 'resolution_type_id', ResolutionType)
        self.update_relate_table('uses', UseRelate, 'use_type_id', UseType)
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
