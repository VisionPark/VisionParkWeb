# Generated by Django 3.2.8 on 2021-11-04 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageParking', '0008_alter_parking_canvas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='canvas',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
