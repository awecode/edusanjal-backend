# Generated by Django 2.0.4 on 2018-05-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0011_auto_20180527_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='previous_db_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
