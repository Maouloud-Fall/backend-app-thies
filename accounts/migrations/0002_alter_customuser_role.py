# Generated by Django 5.2.1 on 2025-05-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('EMPLOYER', 'Employer'), ('USER', 'User')], default='USER', max_length=50),
        ),
    ]
