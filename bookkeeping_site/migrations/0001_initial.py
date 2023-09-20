# Generated by Django 4.2.4 on 2023-09-20 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields.related


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
                ('course', models.FloatField(default=0, verbose_name='Курс')),
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
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('account', models.ForeignKey(on_delete=django.db.models.fields.related.OneToOneField, to='bookkeeping_site.categoryaccounts', unique=True, verbose_name='Cчета')),
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
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('account1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account1', to='bookkeeping_site.useraccount', verbose_name='C счета')),
                ('account2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account2', to='bookkeeping_site.useraccount', verbose_name='На счет счета')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Перевод Пользователя',
                'verbose_name_plural': 'Перевод Пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserOweDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('data_1', models.DateField(verbose_name='С даты')),
                ('data_2', models.DateField(verbose_name='До даты')),
                ('comment', models.CharField(blank=True, max_length=150, null=True, verbose_name='Коментарий')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('initial_sum', models.IntegerField(verbose_name='Первоначальная сумма')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Долги у Пользователя',
                'verbose_name_plural': 'Долги у Пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserIncomes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=20, null=True, verbose_name='Коментарий')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('created_at', models.DateField(verbose_name='Дата')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_incomes', to='bookkeeping_site.categoryincome', verbose_name='Категория')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory_incomes', to='bookkeeping_site.categoryincome', verbose_name='Подкатегория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Доходы пользователя',
                'verbose_name_plural': 'Доходы Пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserExpenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=20, null=True, verbose_name='Коментарий')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('created_at', models.DateField(verbose_name='Дата')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_expenses', to='bookkeeping_site.categoryexpenses', verbose_name='Категория')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory_expenses', to='bookkeeping_site.categoryexpenses', verbose_name='Подкатегория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Расход пользователя',
                'verbose_name_plural': 'Расходы пользователя',
            },
        ),
        migrations.CreateModel(
            name='UserDebt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('data_1', models.DateField(verbose_name='С даты')),
                ('data_2', models.DateField(verbose_name='До даты')),
                ('comment', models.CharField(blank=True, max_length=150, null=True, verbose_name='Коментарий')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('initial_sum', models.IntegerField(verbose_name='Первоначальная сумма')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.useraccount', verbose_name='Счет')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookkeeping_site.categorycurrency', verbose_name='Валюта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Долги Пользователя',
                'verbose_name_plural': 'Долги Пользователя',
            },
        ),
    ]
