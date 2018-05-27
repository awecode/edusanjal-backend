# Generated by Django 2.0.4 on 2018-05-27 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0012_auto_20180515_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institute',
            name='ugc_accredition',
        ),
        migrations.AddField(
            model_name='institute',
            name='featured',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='institute',
            name='is_member',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='institute',
            name='ugc_accreditation',
            field=models.BooleanField(default=False, verbose_name='UGC Accreditation'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='institute.Institute'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='institute.Institute'),
        ),
    ]
