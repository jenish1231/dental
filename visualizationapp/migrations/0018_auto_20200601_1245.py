# Generated by Django 2.1 on 2020-06-01 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationapp', '0017_auto_20200510_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualization',
            name='geography_id',
            field=models.CharField(db_index=True, default='', max_length=60),
        ),
    ]
