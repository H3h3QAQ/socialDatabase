# Generated by Django 3.2.1 on 2021-05-07 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InviteModel', '0002_alter_invitee_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitee',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
    ]