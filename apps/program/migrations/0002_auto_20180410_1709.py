# Generated by Django 2.0.4 on 2018-04-10 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='council',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]