# Generated by Django 3.0.6 on 2020-05-11 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ItemDetail',
            new_name='ItemOrderDetail',
        ),
    ]
