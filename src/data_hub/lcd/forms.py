from django import forms
from django.contrib.admin.widgets import AdminDateWidget

# from django.core.exceptions import ValidationError
# from django.db.utils import ProgrammingError
#
# from .models import (Collection, County, CountyRelate, Product)
from .models import (Collection,
                     BandRelate,
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
#
class CollectionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=60)
    acquisition_date = forms.DateField(required=False, widget=AdminDateWidget())
    known_issues = forms.CharField(required=False, widget=forms.Textarea(), initial='None')
    tile_index_url = forms.ChoiceField(required=False, choices=(('', ''),('T', 'True'),('Lidar', 'Lidar')))
    carto_map_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}),max_length=50)

    overview_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}), initial='images/placeholder.png')
    thumbnail_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}), initial='images/placeholder.png')
    natural_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}))
    urban_image = forms.CharField(required=False, widget=forms.TextInput(attrs={'style':'width:758px'}))

    class Meta:
        model = Collection
        help_texts = {
            'counties': 'Hold down CTRL to add/remove multiple counties.',
        }
        fields = ('__all__')


    # added a try/except for initial migration without data
    # try:
    #     county_choices = (
    #         (c.id, c.name) for c in County.objects.all().order_by("name"))
    # except ProgrammingError:
    #     county_choices = ()
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.initial_counties = []
    #     if self.instance:
    #         self.initial_counties = [
    #             c[0] for c in CountyRelate.objects.values_list(
    #                 "county_id").filter(collection=self.instance.id)
    #         ]
    #         self.fields['counties'].initial = self.initial_counties
    #
    # counties = forms.MultipleChoiceField(
    #     widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple counties',}),
    #     choices=county_choices
    # )
    #
    # def save(self, commit=True):
    #     updated_counties = self.cleaned_data['counties']
    #     initial_counties_str = [
    #         str(u) for u in self.initial_counties
    #     ]
    #     removes = [c for c in initial_counties_str if c not in updated_counties]
    #     adds = [c for c in updated_counties if c not in initial_counties_str]
    #     for remove in removes:
    #         CountyRelate.objects.filter(
    #             county=remove).filter(collection=self.instance.id).delete()
    #     for add in adds:
    #         CountyRelate(county_id=add, collection=self.instance).save()
    #     return super(CollectionForm, self).save(commit=commit)
