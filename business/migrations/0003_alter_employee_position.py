# Generated by Django 3.2.3 on 2022-02-26 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(choices=[('Assistant', 'Assistant'), ('Doctor', 'Doctor'), ('Accountant', 'Accountant'), ('Associate', 'Associate'), ('Pharmasist', 'Pharmasist'), ('Nurse', 'Nurse'), ('Cleaner', 'Cleaner')], default='Assistant', max_length=50, null=True),
        ),
    ]
