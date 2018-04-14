# Generated by Django 2.0.4 on 2018-04-10 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0003_auto_20180410_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutedocument',
            name='file',
            field=models.FileField(upload_to='institute_documents/'),
        ),
        migrations.AlterField(
            model_name='institutedocument',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='institute.Institute'),
        ),
        migrations.AlterField(
            model_name='instituteimage',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='institute.Institute'),
        ),
    ]