# Generated by Django 5.1.3 on 2024-12-17 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('port_data', '0012_rename_client_email_servicerequest_email_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='is_active',
            field=models.BooleanField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='nom',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='prenom',
            field=models.CharField(max_length=200, verbose_name='surname'),
        ),
    ]
