from django import forms
from django.core.exceptions import ValidationError
from django.db.utils import ProgrammingError

from .models import Collection, County, CountyRelate, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    clean_status = forms.BooleanField(label='Clean Status', help_text='Clean Status refers to collections that have been reviewed and are ready to been scanned, no erasing of frames needed. Default is False/Unchecked.')

    def clean(self):
        try:
            if (self.cleaned_data.get('number_of_frames')
                    < self.cleaned_data.get('scanned')):
                raise ValidationError("Scanned must be >= number of frames")
        except Exception:
            raise ValidationError("Scanned must be >= number of frames")
        return self.cleaned_data


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        help_texts = {
            'counties': 'Hold down CTRL to add/remove multiple counties.',
        }
        fields = ('collection', 'agency', 'from_date', 'to_date', 'counties',
                  'remarks')

    # added a try/except for initial migration without data
    try:
        county_choices = (
            (c.id, c.name) for c in County.objects.all().order_by("name"))
    except ProgrammingError:
        county_choices = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_counties = []
        if self.instance:
            self.initial_counties = [
                c[0] for c in CountyRelate.objects.values_list(
                    "county_id").filter(collection=self.instance.id)
            ]
            self.fields['counties'].initial = self.initial_counties

    counties = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'title': 'Hold down ctrl to select multiple counties',}),
        choices=county_choices
    )

    def clean(self):
        index = self.cleaned_data['index_service_url']
        frames = self.cleaned_data['frames_service_url']
        mosaic = self.cleaned_data['mosaic_service_url']

        links = []
        if index is not None:
            if '_index' not in index:
                raise forms.ValidationError('That is not an Index Service URL!')
            idx_link = index.split('/')[-1].replace('.map', '').replace('_index', '').replace('_', ' ').upper()
            if idx_link not in links:
                links.append(idx_link)
        if frames is not None:
            if '_frames' not in frames:
                raise forms.ValidationError('That is not an Frames Service URL!')
            frm_link = frames.split('/')[-1].replace('.map', '').replace('_frames', '').replace('_', ' ').upper()
            if frm_link not in links:
                links.append(frm_link)
        if mosaic is not None:
            if '_mosaic' not in mosaic:
                raise forms.ValidationError('That is not an Mosaic Service URL!')
            msc_link = mosaic.split('/')[-1].replace('.map', '').replace('_mosaic', '').replace('_', ' ').upper()
            if msc_link not in links:
                links.append(msc_link)
        if len(links) > 1:
            raise forms.ValidationError('Index, Frames, and Mosaic Service URLs have inconsistent collections!')
        elif len(links) == 1:
            self.instance.ls4_link = links[0]
        else:
            self.instance.ls4_link = None

    def save(self, commit=True):
        updated_counties = self.cleaned_data['counties']
        initial_counties_str = [
            str(u) for u in self.initial_counties
        ]
        removes = [c for c in initial_counties_str if c not in updated_counties]
        adds = [c for c in updated_counties if c not in initial_counties_str]
        for remove in removes:
            CountyRelate.objects.filter(
                county=remove).filter(collection=self.instance.id).delete()
        for add in adds:
            CountyRelate(county_id=add, collection=self.instance).save()
        return super(CollectionForm, self).save(commit=commit)
