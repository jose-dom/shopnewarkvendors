# Generated by Django 3.0.3 on 2020-05-22 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200521_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics', verbose_name='<strong>Business Logo</strong>&nbsp;'),
        ),
        migrations.AlterField(
            model_name='user',
            name='business_structure',
            field=models.CharField(choices=[('Sole Proprietorship', 'Sole Proprietorship'), ('Limited Liability Corporation', 'Limited Liability Corporation'), ('S Corp', 'S Corp'), ('Other', 'Other')], max_length=1000, verbose_name='Business Structure'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=60, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text='Ex: 800-786-8765', max_length=12, verbose_name='Contact Phone Number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tax_credits',
            field=models.CharField(choices=[('On line, manually (Free)', 'On line, manually (Free)'), ('Downloading the application onto my own Android (Free)', 'Downloading the application onto my own Android (Free)'), ('Fincredit’s Dedicated Device and Stand ($90)', 'Fincredit’s Dedicated Device and Stand ($90)')], max_length=1000, verbose_name='Tax Credits'),
        ),
    ]
