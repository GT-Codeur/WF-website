# Generated by Django 3.2.2 on 2021-05-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0029_rename_page_number_archivearticle_toc_page_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivearticle',
            name='drupal_node_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]