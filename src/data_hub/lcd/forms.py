from django import forms
from django.contrib.admin.widgets import AdminDateWidget

# from django.core.exceptions import ValidationError
from django.db.utils import ProgrammingError
#
# from .models import (Collection, County, CountyRelate, Product)
from .models import (Collection,
                     BandRelate,
                     BandType,
                     CategoryRelate,
                     DataTypeRelate,
                     EpsgRelate,
                     FileTypeRelate,
                     ResolutionRelate,
                     UseRelate)
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


class CollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        help_texts = {
            'counties': 'Hold down CTRL to add/remove multiple counties.',
        }
        fields = ('__all__')

    name = forms.CharField(widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=150)
    acquisition_date = forms.DateField(required=False, widget=AdminDateWidget())
    known_issues = forms.CharField(required=False, widget=forms.Textarea(), initial='None')
    carto_map_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=50)

    overview_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}), initial='images/placeholder.png')
    thumbnail_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}), initial='images/placeholder.png')
    natural_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}))
    urban_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}))

    def create_relate_field(id_field, label_field, type_table, order_field):
        # added a try/except for initial migration without data
        try:
            choices = (
                (getattr(b, id_field), getattr(b, label_field)) for b in type_table.objects.all().order_by(order_field))
        except ProgrammingError:
            choices = ()

        input = forms.MultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple values',}),
            choices=choices
        )
        return input

    bands = create_relate_field('band_type_id', 'band_name', BandType, 'band_name')

    def attribute_initial_values(self, name, relate_table, id_field):
        attr_name = 'initial_' + name
        setattr(self, attr_name, [])
        setattr(self, attr_name, [
            b[0] for b in relate_table.objects.values_list(id_field).filter(collection_id=self.instance.collection_id)
        ])
        self.fields[name].initial = getattr(self, attr_name)
        return

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.attribute_initial_values('bands', BandRelate, 'band_type_id')

    def update_relate_table(self, name, relate_table, id_field, type_table):
        attr_name = 'initial_' + name

        updated = self.cleaned_data[name]
        initial_str = [
            str(u) for u in getattr(self, attr_name)
        ]
        removes = [b for b in initial_str if b not in updated]
        adds = [b for b in updated if b not in initial_str]
        for remove in removes:
            args = {}
            args[id_field] = remove
            relate_table.objects.filter(
                **args).filter(collection_id=self.instance.collection_id).delete()
        for add in adds:
            collection_record = Collection.objects.get(collection_id=self.instance.collection_id)
            args = {'collection_id': collection_record}

            type_arg = {}
            type_arg[id_field] = add
            type_record = type_table.objects.get(**type_arg)
            args[id_field] = type_record

            relate_table(**args).save()
        return

    def save(self, commit=True):
        self.update_relate_table('bands', BandRelate, 'band_type_id', BandType)
        return super(CollectionForm, self).save(commit=commit)
