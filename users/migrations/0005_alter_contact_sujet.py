# Generated by Django 4.2.1 on 2024-01-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_contact_sujet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="sujet",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]