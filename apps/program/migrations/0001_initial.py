# Generated by Django 2.0.4 on 2018-04-10 10:17

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('short_name', models.CharField(blank=True, max_length=15, null=True)),
                ('established', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1700), django.core.validators.MaxValueValidator(2050)])),
                ('address', models.TextField(blank=True, null=True)),
                ('logo', versatileimagefield.fields.VersatileImageField(upload_to='boards/')),
                ('phone', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100, null=True), blank=True, null=True, size=None)),
                ('email', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=254, null=True), blank=True, null=True, size=None)),
                ('website', models.URLField(blank=True, null=True)),
                ('video_link', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('salient_features', models.TextField(blank=True, null=True)),
                ('international', models.BooleanField(default=False)),
                ('documents', models.ManyToManyField(blank=True, to='media.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('short_name', models.CharField(blank=True, max_length=255, null=True)),
                ('duration_years', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('duration_months', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField()),
                ('eligibility', models.TextField(blank=True, null=True)),
                ('job_prospects', models.TextField(blank=True, null=True)),
                ('salient_features', models.TextField(blank=True, null=True)),
                ('curricular_stucture', models.TextField(blank=True, null=True)),
                ('admission_criteria', models.TextField(blank=True, null=True)),
                ('featured', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=True)),
                ('board', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='program.Board')),
                ('disciplines', models.ManyToManyField(blank=True, related_name='programs', to='program.Discipline')),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='program.Faculty')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.Level')),
                ('recognition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='program.Council')),
                ('related_programs', models.ManyToManyField(blank=True, related_name='_program_related_programs_+', to='program.Program')),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='faculties',
            field=models.ManyToManyField(blank=True, to='program.Faculty'),
        ),
        migrations.AddField(
            model_name='board',
            name='images',
            field=models.ManyToManyField(blank=True, to='media.Image'),
        ),
    ]