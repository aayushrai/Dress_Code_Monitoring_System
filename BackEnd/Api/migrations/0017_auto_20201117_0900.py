# Generated by Django 3.0.7 on 2020-11-17 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0016_auto_20201117_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='emailed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(upload_to='Faces/2020-11-17-09-00-05'),
        ),
    ]