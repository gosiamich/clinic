# Generated by Django 3.0.6 on 2022-03-19 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=128)),
                ('postcode', models.CharField(max_length=6)),
                ('street', models.CharField(max_length=128)),
                ('building_number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('phone_number', models.PositiveIntegerField()),
                ('email', models.CharField(blank=True, max_length=128)),
                ('address', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.PositiveIntegerField(blank=True)),
                ('address', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Address')),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Specialization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(1, 'Poniedziałek'), (2, 'Wtorek'), (3, 'Środa'), (4, 'Czwartek'), (5, 'Piątek')])),
                ('sch_from', models.TimeField()),
                ('sch_to', models.TimeField()),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Clinic')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Specialist')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pesel', models.CharField(max_length=11, unique=True)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=55)),
                ('phone_number', models.PositiveIntegerField(blank=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Address')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='clinic',
            name='specialists',
            field=models.ManyToManyField(through='doctor_app.Schedule', to='doctor_app.Specialist'),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_date', models.DateField()),
                ('a_from', models.TimeField()),
                ('a_to', models.TimeField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Patient')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Specialist')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor_app.Type')),
            ],
        ),
    ]
