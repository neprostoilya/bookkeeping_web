# Generated by Django 4.2.4 on 2023-09-23 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookkeeping_site', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserDebt',
            new_name='UserDebts',
        ),
        migrations.RenameModel(
            old_name='UserOweDebt',
            new_name='UserOweDebts',
        ),
        migrations.CreateModel(
            name='CategoryIncomes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название категории дохода')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='bookkeeping_site.categoryincomes', verbose_name='Категория')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Категория Дохода',
                'verbose_name_plural': 'Категории Доходов',
            },
        ),
        migrations.AlterField(
            model_name='userincomes',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_incomes', to='bookkeeping_site.categoryincomes', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='userincomes',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory_incomes', to='bookkeeping_site.categoryincomes', verbose_name='Подкатегория'),
        ),
        migrations.DeleteModel(
            name='CategoryIncome',
        ),
    ]
