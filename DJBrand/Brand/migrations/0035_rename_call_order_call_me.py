# Generated by Django 4.2 on 2023-09-29 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0034_order_call'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='call',
            new_name='call_me',
        ),
    ]
