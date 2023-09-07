import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class CategoryIncome(models.Model):
    """Категории доходов по дефолту"""
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории дохода'
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
        return f'Категория: pk={self.pk}, title={self.title}, parent={self.parent}'
    
    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория Дохода'
        verbose_name_plural = 'Категории Доходов'

class CategoryExpenses(models.Model):
    """Категории расходов по дефолту"""
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории расхода'
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
        return f'Категория: pk={self.pk}, title={self.title}, parent={self.parent}'
    
    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория Расхода'
        verbose_name_plural = 'Категории Расходов'

class CategoryCurrency(models.Model):
    """Категории единиц валют"""
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории валюты'
    )
    course = models.FloatField(
        default=0,
        null=False,
        verbose_name='Курс'
    )
    def __str__(self):
        """Строковое представление"""
        return self.title
    
    def __repr__(self):
        """Подобие строкового представления"""
        return f'Категория: pk={self.pk}, title={self.title}'
    
    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория Валюты'
        verbose_name_plural = 'Категории Валют'

class CategoryAccounts(models.Model):
    """Категории счетов по дефолту"""
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории'
    )
    def __str__(self):
        """Строковое представление"""
        return str(self.title)

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория Счета'
        verbose_name_plural = 'Категории Счетов'

class UserAccount(models.Model):
    """Счета пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    account = models.ForeignKey(
        CategoryAccounts,
        on_delete=models.OneToOneField,
        null=False,
        unique=True,
        verbose_name='Cчета'
    )
    currency = models.ForeignKey(
        CategoryCurrency,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    sum = models.IntegerField(
        verbose_name='Сумма'
    )

    def get_absolute_url(self): 
        return reverse('update_account', args=[str(self.id)])

    def __str__(self):
        """Строковое представление"""
        return self.account.title
    
    def __repr__(self):
        """Подобие строкового представления"""
        return f'Счет: pk={self.pk}, account={self.account}, course={self.currency.course}, currency={self.currency}, sum={self.sum}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Счет Пользователя'
        verbose_name_plural = 'Счета Пользователя'

    @property # используется для создания <<специальной>> функциональности определеным методам
    def get_course_sum(self):
        """Получение полной суммы счета с учетом курса валют"""
        sum = self.sum
        course = self.currency.course
        return course*sum
    
class UserExpenses(models.Model):
    """Расходы пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name='Пользователь'
    )
    category = models.ForeignKey(
        CategoryExpenses,
        related_name='category_expenses',
        on_delete=models.CASCADE, 
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        CategoryExpenses,
        related_name='subcategory_expenses',
        on_delete=models.CASCADE, 
        verbose_name='Подкатегория',
        null=True,
        blank=True
    )
    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name='Счет'
    )
    comment = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    currency = models.ForeignKey(
        CategoryCurrency,
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    sum = models.IntegerField(
        verbose_name='Сумма'
    )
    created_at = models.DateField(
        verbose_name='Дата'
    )

    def __str__(self):
        """Строковое представление"""
        return self.user.username

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Расход: pk={self.pk}, category={self.category}, subcategory={self.subcategory}, account={self.account}, currency={self.currency} sum={self.sum}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Расход пользователя'
        verbose_name_plural = 'Расходы пользователя'

    @property
    def get_total_sum_expenses(self):
        """Получение полной суммы расхода"""
        sum = self.sum
        currency = self.currency.course
        return sum * currency
    
class UserIncomes(models.Model):
    """Доходы пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name='Пользователь'
    )
    category = models.ForeignKey(
        CategoryIncome,
        related_name='category_incomes',
        on_delete=models.CASCADE, 
        verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        CategoryIncome,
        related_name='subcategory_incomes',
        on_delete=models.CASCADE, 
        verbose_name='Подкатегория',
        null=True,
        blank=True
    )
    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name='Счет'
    )
    comment = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    currency = models.ForeignKey(
        CategoryCurrency,
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    sum = models.IntegerField(
        verbose_name='Сумма'
    )
    created_at = models.DateField(
        verbose_name='Дата'
    )

    def __str__(self):
        """Строковое представление"""
        return self.user.username

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Доходы: pk={self.pk}, category={self.category}, subcategory={self.subcategory}, account={self.account}, currency={self.currency} sum={self.sum}'
    
    class Meta:
        """Характер Класса"""
        verbose_name = 'Доходы пользователя'
        verbose_name_plural = 'Доходы Пользователя'
    
    @property
    def get_total_sum_income(self):
        """Получение полной суммы дохода"""
        sum = self.sum
        currency = self.currency.course
        return sum * currency

class UserTransferToAccount(models.Model):
    """Переводы пользователя с счета на счет"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    account1 = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='account1',
        null=False,
        verbose_name='C счета'
    )
    account2 = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name='account2',
        null=False,
        verbose_name='На счет счета'
    )
    sum = models.IntegerField(
        verbose_name='Сумма'
    )

    def __str__(self):
        """Строковое представление"""
        return self.user.username
    
    def __repr__(self):
        """Подобие строкового представления"""
        return f'Переводы: pk={self.pk}, account1={self.account1}, account2={self.account2},  sum={self.sum}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Перевод Пользователя'
        verbose_name_plural = 'Перевод Пользователя'
    
class UserOweDebt(models.Model):
    """Долги y пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    name = models.CharField(
        null=False,
        max_length=100,
        verbose_name='Имя'
    )
    data_1 = models.DateField(
        verbose_name='С даты'
    )
    data_2 = models.DateField(
        verbose_name='До даты'
    )
    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name='Счет'
    )
    comment = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    currency = models.ForeignKey(
        CategoryCurrency,
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    sum = models.IntegerField(
        verbose_name='Сумма'
    )

    def __str__(self):
        """Строковое представление"""
        return self.user.username
    
    def __repr__(self):
        """Подобие строкового представления"""
        return f'Переводы: pk={self.pk}, data_1={self.data_1}, data_2={self.data_2},    \
                account={self.account}, currency={self}, comment={self.comment}, sum={self.sum}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Долги у Пользователя'
        verbose_name_plural = 'Долги у Пользователя'

class UserDebt(models.Model):
    """Долги пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    name = models.CharField(
        null=False,
        max_length=100,
        verbose_name='Имя'
    )
    data_1 = models.DateField(
        verbose_name='С даты'
    )
    data_2 = models.DateField(
        verbose_name='До даты'
    )
    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name='Счет'
    )
    comment = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    currency = models.ForeignKey(
        CategoryCurrency,
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    sum = models.IntegerField(
        verbose_name='Сумма'
    )

    def __str__(self):
        """Строковое представление"""
        return self.user.username
    
    def __repr__(self):
        """Подобие строкового представления"""
        return f'Переводы: pk={self.pk}, data_1={self.data_1}, data_2={self.data_2},    \
                account={self.account}, currency={self}, comment={self.comment}, sum={self.sum}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Долги Пользователя'
        verbose_name_plural = 'Долги Пользователя'