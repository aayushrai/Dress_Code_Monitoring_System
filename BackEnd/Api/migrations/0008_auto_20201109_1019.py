# Generated by Django 3.0.7 on 2020-11-09 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0007_auto_20201109_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(upload_to='Faces/2020-11-09-10-19-08'),
        ),
    ]
