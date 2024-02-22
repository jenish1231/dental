# Generated by Django 2.0 on 2019-11-22 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationapp', '0008_auto_20191120_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visualization',
            name='decayed_permanent_teeth_number',
            field=models.PositiveIntegerField(default=0, verbose_name='decayed permanent teeth'),
        ),
        migrations.AlterField(
            model_name='visualization',
            name='decayed_primary_teeth_number',
            field=models.PositiveIntegerField(default=0, verbose_name='decayed primary teeth'),
        ),
    ]
