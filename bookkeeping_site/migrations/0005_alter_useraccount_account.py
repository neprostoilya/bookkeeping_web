# Generated by Django 4.2.4 on 2023-09-02 19:37

from django.db import migrations, models
import django.db.models.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping_site', '0004_alter_useraccount_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.fields.related.OneToOneField, to='bookkeeping_site.categoryaccounts', unique=True, verbose_name='Cчета'),
        ),
    ]