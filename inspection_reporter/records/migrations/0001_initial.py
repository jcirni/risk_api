# Generated by Django 3.0.3 on 2020-02-13 00:30

from django.db import migrations, models
import django.db.models.deletion
import inspection_reporter.utils.records_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('score', models.IntegerField()),
                ('comments', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('street_address', models.TextField(validators=[inspection_reporter.utils.records_validators.is_valid_address])),
                ('city', models.TextField()),
                ('state', models.CharField(max_length=2, validators=[inspection_reporter.utils.records_validators.is_valid_state_abbrev])),
                ('postal_code', models.CharField(max_length=5, validators=[inspection_reporter.utils.records_validators.is_valid_zip])),
                ('is_current', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_critical', models.BooleanField()),
                ('code', models.TextField()),
                ('description', models.TextField()),
                ('comments', models.TextField(blank=True, default='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RestaurantInspectionViolations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('average_violations', models.DecimalField(decimal_places=2, max_digits=5)),
                ('inspection_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Inspection')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Restaurant')),
                ('violation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Violation')),
            ],
        ),
        migrations.AddField(
            model_name='inspection',
            name='restaurant_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Restaurant'),
        ),
    ]
