# Generated by Django 3.2.1 on 2021-05-05 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InfoModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='identity',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]