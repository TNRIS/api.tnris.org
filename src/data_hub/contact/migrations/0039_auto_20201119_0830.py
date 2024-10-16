# Generated by Django 3.0.8 on 2020-11-19 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0038_auto_20201015_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveytemplate',
            name='content_type',
            field=models.CharField(choices=[('single-modal', 'single-modal'), ('multi-modal', 'multi-modal')], default='multi-modal', help_text='Only the Full Modal content will display in the case that `single` is selected. Upon exiting the modal, the modal will close and will not be displayed to the user again', max_length=16, verbose_name='The display type of the modal; for example, should it display a series of dialogues, or should the modal be a single, static-text alert type.'),
        ),
        migrations.AddField(
            model_name='surveytemplate',
            name='dev_mode',
            field=models.BooleanField(default=False, verbose_name='Boolean value, if true, the modal will only display in development'),
        ),
    ]
