# Generated by Django 3.1.1 on 2021-01-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_auto_20201229_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donor_family_name',
            field=models.CharField(default='Name', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donation',
            name='donor_given_name',
            field=models.CharField(default='Family', max_length=255),
            preserve_default=False,
        ),
    ]