# Generated by Django 2.0.4 on 2018-05-08 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0016_auto_20180508_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='previous_db_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
