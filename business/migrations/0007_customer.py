# Generated by Django 3.2.3 on 2022-03-03 02:16

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0006_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', phone_field.models.PhoneField(help_text='Contact phone number', max_length=31)),
                ('email', models.EmailField(max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/CustomerProfilePic/')),
                ('address', models.CharField(max_length=40)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Femele', 'Femele'), ('Other', 'Other')], default='Femele', max_length=50, null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('info', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
