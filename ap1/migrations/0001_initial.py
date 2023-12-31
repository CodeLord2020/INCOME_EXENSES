# Generated by Django 4.1.7 on 2023-06-21 22:58

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
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('Salary', 'Salary'), ('Allowance', 'Allowance'), ('Hustle', 'Hustle'), ('Ritual', 'Ritual'), ('Others', 'Others')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, max_length=220)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Gadgets', 'Gadgets'), ('Books', 'Books'), ('Home', 'Home'), ('Internet', 'Internet'), ('Transport', 'Transport'), ('Food', 'Food'), ('Others', 'Others')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, max_length=220)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
