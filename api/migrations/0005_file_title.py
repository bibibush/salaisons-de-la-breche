# Generated by Django 4.2.1 on 2023-05-24 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
