# Generated by Django 2.2.1 on 2019-05-20 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exhibit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exhibit.User'),
        ),
    ]
