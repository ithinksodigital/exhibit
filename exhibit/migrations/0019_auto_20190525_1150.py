# Generated by Django 2.2.1 on 2019-05-25 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibit', '0018_auto_20190525_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendmessage',
            name='msgtitle',
            field=models.CharField(default='Wiadomość ze strony', max_length=100),
        ),
    ]
