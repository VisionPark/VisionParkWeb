# Generated by Django 3.1.7 on 2021-09-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageParking', '0005_auto_20210721_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='since',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='space',
            name='vacant',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
