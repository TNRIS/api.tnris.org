from django import forms
# from django.core.exceptions import ValidationError
# from django.db.utils import ProgrammingError

from .models import MapCollection, MapDataRelate
from lcd.models import Collection


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


class MapCollectionForm(forms.ModelForm):
    class Meta:
        model = MapCollection
        help_texts = {
            'data_collections': 'Hold down CTRL to add/remove multiple data collections.',
        }
        fields = ('name', 'publish_date', 'description', 'public',
                  'thumbnail_link', 'data_collections')

    # added a try/except for initial migration without data
    try:
        data_collection_choices = (
            (c.collection_id, str(c.acquisition_date)[:4].replace('None', '') + ' ' + c.name) for c in Collection.objects.all().order_by("name", "acquisition_date")
            )
    except ProgrammingError:
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

    def save(self, commit=True):
        updated_data_collections = self.cleaned_data['data_collections']
        initial_data_collections_str = [
            str(u) for u in self.initial_data_collections
        ]
        removes = [c for c in initial_data_collections_str if c not in updated_data_collections]
        adds = [c for c in updated_data_collections if c not in initial_data_collections_str]
        print(removes)
        print(adds)
        for remove in removes:
            MapDataRelate.objects.filter(
                data_collection_id=remove).filter(map_collection_id=self.instance).delete()
        for add in adds:
            data_collection_rec = Collection.objects.get(collection_id=add)
            MapDataRelate(data_collection_id=data_collection_rec, map_collection_id=self.instance).save()
        return super(MapCollectionForm, self).save(commit=commit)
