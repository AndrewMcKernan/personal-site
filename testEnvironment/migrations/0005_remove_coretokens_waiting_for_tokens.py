# Generated by Django 4.0 on 2025-01-21 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testEnvironment', '0004_alter_coretokens_access_token_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coretokens',
            name='waiting_for_tokens',
        ),
    ]
