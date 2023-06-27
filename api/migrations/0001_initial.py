# Generated by Django 4.2.1 on 2023-06-27 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True)),
                ('file', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, verbose_name='nom')),
                ('prenom', models.CharField(max_length=50, verbose_name='prenom')),
                ('adresse', models.CharField(max_length=50, verbose_name='adresse')),
                ('phonenumber', models.CharField(max_length=50, verbose_name='phonenumber')),
                ('entreprise', models.CharField(max_length=100, verbose_name='entreprise')),
                ('email', models.CharField(max_length=50, verbose_name='email')),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='create date')),
                ('modify_dt', models.DateField(auto_now=True, verbose_name='modify date')),
                ('order_file', models.FileField(null=True, upload_to='upload/')),
                ('order_number', models.CharField(blank=True, max_length=10, verbose_name='order number')),
                ('date', models.DateField(null=True)),
                ('pay', models.BooleanField(default=False)),
                ('block', models.BooleanField(default=False)),
            ],
        ),
    ]
