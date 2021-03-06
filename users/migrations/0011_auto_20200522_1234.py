# Generated by Django 3.0.3 on 2020-05-22 16:34

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200521_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='speical_business',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Minority Owned', 'Minority Owned'), ('Woman Owned', 'Woman Owned'), ('MWBE Certified', 'MWBE Certified'), ('DBE Certified', 'DBE Certified'), ('VOSBE Certified', 'VOSBE Certified')], max_length=71, verbose_name='Is your business: (Check all that apply)'),
        ),
    ]
