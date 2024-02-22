# Generated by Django 2.0 on 2019-11-20 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizationapp', '0006_auto_20191115_0301'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualization',
            name='sdf_whole_mouth',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='visualization',
            name='decayed_permanent_teeth',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='decayed permanent teeth'),
        ),
        migrations.AlterField(
            model_name='visualization',
            name='decayed_primary_teeth',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='decayed primary teeth'),
        ),
    ]