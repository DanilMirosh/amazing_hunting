# Generated by Django 4.1.3 on 2022-11-12 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0005_skill_is_acnive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skill',
            old_name='is_acnive',
            new_name='is_active',
        ),
    ]
