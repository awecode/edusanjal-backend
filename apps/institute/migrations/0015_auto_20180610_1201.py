# Generated by Django 2.0.4 on 2018-06-10 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0014_auto_20180608_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='boards',
            field=models.ManyToManyField(blank=True, related_name='institutes', to='program.Board'),
        ),
    ]
