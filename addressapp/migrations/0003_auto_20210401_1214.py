# Generated by Django 2.1 on 2021-04-01 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressapp', '0002_auto_20200113_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ward',
            name='name',
            field=models.CharField(blank=True, db_index=True, default='', max_length=50),
        ),
    ]