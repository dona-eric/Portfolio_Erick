# Generated by Django 5.1.3 on 2024-12-01 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('port_data', '0007_articles_author_articles_articles_categorie_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Articles',
            new_name='Article',
        ),
        migrations.RenameModel(
            old_name='Contacts',
            new_name='Contact',
        ),
        migrations.RenameModel(
            old_name='Projects',
            new_name='Project',
        ),
        migrations.RenameModel(
            old_name='Services',
            new_name='Service',
        ),
        migrations.RenameModel(
            old_name='Skills',
            new_name='Skill',
        ),
    ]