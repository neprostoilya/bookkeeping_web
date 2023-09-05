# Generated by Django 4.2.4 on 2023-09-05 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookkeeping_site', '0007_userdebt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdebt',
            options={'verbose_name': 'Долги Пользователя', 'verbose_name_plural': 'Долги Пользователя'},
        ),
        migrations.AlterField(
            model_name='userdebt',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет'),
        ),
        migrations.CreateModel(
            name='UserOweDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('data_1', models.DateField(verbose_name='С даты')),
                ('data_2', models.DateField(verbose_name='До даты')),
                ('comment', models.CharField(blank=True, max_length=150, null=True)),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Долги у Пользователя',
                'verbose_name_plural': 'Долги у Пользователя',
            },
        ),
    ]
