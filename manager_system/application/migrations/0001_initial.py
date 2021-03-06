# Generated by Django 4.0.5 on 2022-07-08 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_period', models.DateField()),
                ('end_period', models.DateField()),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Periods',
                'db_table': 'period',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='period', to='application.period')),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
                'db_table': 'schedule',
            },
        ),
        migrations.CreateModel(
            name='WorkerTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_str', models.CharField(blank=True, max_length=100, null=True)),
                ('day_num', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('additional_hours_start_time', models.TimeField(blank=True, null=True)),
                ('additional_hours_end_time', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'WorkerTime',
                'verbose_name_plural': 'WorkerTimes',
                'db_table': 'worker_time',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')),
                ('rating', models.CharField(max_length=100)),
                ('reviews', models.CharField(max_length=100)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='application.location')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='application.category')),
                ('date', models.ManyToManyField(blank=True, to='application.schedule')),
            ],
            options={
                'verbose_name': 'Wpecialist',
                'verbose_name_plural': 'Worker',
                'db_table': 'Worker',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='period',
            name='worker_time',
            field=models.ManyToManyField(blank=True, related_name='worker_time', to='application.workertime'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='application.customer')),
                ('worker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='application.worker')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
                'db_table': 'appointment',
                'ordering': ['id'],
            },
        ),
    ]
