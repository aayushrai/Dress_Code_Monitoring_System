# Generated by Django 3.0.7 on 2020-11-17 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0012_auto_20201116_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(upload_to='Faces/2020-11-17-07-05-28'),
        ),
    ]
