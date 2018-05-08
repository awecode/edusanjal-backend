# Generated by Django 2.0.4 on 2018-05-08 09:06

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0008_auto_20180508_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='council',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='council',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='council',
            name='logo',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='councils/'),
        ),
        migrations.AddField(
            model_name='council',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='council',
            name='short_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='council',
            name='website',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
