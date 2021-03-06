# Generated by Django 3.0.3 on 2020-02-17 22:52

from django.db import migrations, models
import inspection_reporter.utils.records_validators


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='inspection_id',
            field=models.IntegerField(unique=True, validators=[inspection_reporter.utils.records_validators.valid_id]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='restaurant_id',
            field=models.IntegerField(unique=True, validators=[inspection_reporter.utils.records_validators.valid_id]),
        ),
        migrations.AlterField(
            model_name='violation',
            name='violation_id',
            field=models.IntegerField(unique=True, validators=[inspection_reporter.utils.records_validators.valid_id]),
        ),
    ]
