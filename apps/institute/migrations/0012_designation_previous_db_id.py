# Generated by Django 2.0.4 on 2018-05-08 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0011_institute_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='previous_db_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]