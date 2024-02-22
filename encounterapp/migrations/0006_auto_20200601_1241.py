# Generated by Django 2.1 on 2020-06-01 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encounterapp', '0005_auto_20200527_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encounter',
            name='geography',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='encounter_geography', to='addressapp.Ward'),
        ),
    ]