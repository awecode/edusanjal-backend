# Generated by Django 2.0.4 on 2018-05-10 10:12

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0004_auto_20180510_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituteimage',
            name='file',
            field=versatileimagefield.fields.VersatileImageField(upload_to='institute_images/'),
        ),
    ]
