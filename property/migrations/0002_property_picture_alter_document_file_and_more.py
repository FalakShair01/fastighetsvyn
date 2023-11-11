# Generated by Django 4.2.6 on 2023-11-11 21:20

from django.db import migrations, models
import property.models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=property.models.picture_upload),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=property.models.document_upload),
        ),
        migrations.AlterField(
            model_name='property',
            name='bta',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='geo_energi',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='installered_effekt',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='loa',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='lokal_elproduktion',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='property',
            name='yta',
            field=models.IntegerField(),
        ),
    ]
