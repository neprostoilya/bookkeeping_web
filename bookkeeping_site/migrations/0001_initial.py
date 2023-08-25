# Generated by Django 4.2.4 on 2023-08-25 15:37

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
            name='CategoryAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название категории')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категория Счета',
                'verbose_name_plural': 'Категории Счетов',
            },
        ),
        migrations.CreateModel(
            name='CategoryCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название категории валюты')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категория Валюты',
                'verbose_name_plural': 'Категории Валют',
            },
        ),
        migrations.CreateModel(
            name='CategoryExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название категории расхода')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='bookkeeping_site.categoryexpenses', verbose_name='Категория')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категория Расхода',
                'verbose_name_plural': 'Категории Расходов',
            },
        ),
        migrations.CreateModel(
            name='CategoryIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название категории дохода')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='bookkeeping_site.categoryincome', verbose_name='Категория')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категория Дохода',
                'verbose_name_plural': 'Категории Доходов',
            },
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.FloatField(verbose_name='Курс')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categoryaccounts', verbose_name='Cчета')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Счет Пользователя',
                'verbose_name_plural': 'Счета Пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserTransferToAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.FloatField(verbose_name='Курс')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('account1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account1', to='bookkeeping_site.useraccount', verbose_name='C счета')),
                ('account2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account2', to='bookkeeping_site.useraccount', verbose_name='На счет счета')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Перевод Денег Пользователя',
                'verbose_name_plural': 'Переводы Денег Пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserIncomes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Дата')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categoryincome', verbose_name='Категория')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Доходы пользователя',
                'verbose_name_plural': 'Доходы пользователей',
            },
        ),
        migrations.CreateModel(
            name='UserExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Дата')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categoryexpenses', verbose_name='Категория')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Расход пользователя',
                'verbose_name_plural': 'Расходы пользователей',
            },
        ),
    ]