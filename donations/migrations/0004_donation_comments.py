# Generated by Django 4.2.4 on 2023-08-05 11:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("donations", "0003_alter_donoraddress_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="comments",
            field=models.TextField(
                blank=True, help_text="Comments or instructions about your payment."
            ),
        ),
    ]