# Generated by Django 4.1.4 on 2022-12-21 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_rename_advertisement_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image',
            field=models.ImageField(max_length=1500, null=True, upload_to=''),
        ),
    ]
