# Generated by Django 4.2.1 on 2023-06-21 08:32

import datetime
from django.db import migrations, models
import subscription.models


class Migration(migrations.Migration):
    dependencies = [
        (
            "subscription",
            "0001_squashed_0003_rename_format_subscription_magazine_format",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="end_date",
            field=models.DateField(default=subscription.models.one_year_from_today),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="start_date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]