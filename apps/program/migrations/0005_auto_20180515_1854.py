# Generated by Django 2.0.4 on 2018-05-15 13:09

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0004_auto_20180415_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='description',
            field=froala_editor.fields.FroalaField(),
        ),
        migrations.AlterField(
            model_name='board',
            name='salient_features',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='council',
            name='description',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='description',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='admission_criteria',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='curricular_stucture',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='description',
            field=froala_editor.fields.FroalaField(),
        ),
        migrations.AlterField(
            model_name='program',
            name='eligibility',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='job_prospects',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='salient_features',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
    ]
