# Generated by Django 3.0.7 on 2020-11-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0015_auto_20201117_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(upload_to='Faces/2020-11-17-08-59-20'),
        ),
    ]
