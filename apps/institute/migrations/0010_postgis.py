from django.db import migrations
from django.contrib.postgres.operations import CreateExtension


class Migration(migrations.Migration):
    dependencies = [
        ('institute', '0009_auto_20180430_1653'),
    ]

    operations = [
        CreateExtension('postgis'),
    ]
