from django.db import models
from django.contrib.auth.models import User

class CategoryIncome(models.Model):
    """Категории доходов по дефолту"""
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='subcategories'
    )
    def __str__(self):
        """Строковое представление"""
        return self.title

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория Дохода'
        verbose_name_plural = 'Категории Доходов'

class CategoryExpenses(models.Model):
    """Категории расходовпо дефолту"""
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='subcategories'
    )

    def __str__(self):
        """Строковое представление"""
        return self.title

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория Расхода'
        verbose_name_plural = 'Категории Расходов'

class CategoryAccounts(models.Model):
    """Категории счетов по дефолту"""
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории'
    )
    def __str__(self):
        """Строковое представление"""
        return self.title

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория Счета'
        verbose_name_plural = 'Категории Счетов'

# TODO доделать логику