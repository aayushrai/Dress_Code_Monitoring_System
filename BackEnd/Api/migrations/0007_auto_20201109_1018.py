# Generated by Django 3.0.7 on 2020-11-09 10:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0006_auto_20201108_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(default=uuid.uuid4, max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(upload_to='Faces/2020-11-09-10-18-32'),
        ),
    ]
