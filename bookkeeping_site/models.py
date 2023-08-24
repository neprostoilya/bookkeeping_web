from django.db import models
from django.contrib.auth.models import User

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
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Cчета'
    )
    course = models.FloatField(
        null=False,
        verbose_name='Курс'
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

    def __str__(self):
        """Строковое представление"""
        return self.account.title
    
    def __repr__(self):
        """Подобие строкового представления"""
        return f'Категория: pk={self.pk}, account={self.account}, currency={self.currency}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Счет Пользователя'
        verbose_name_plural = 'Счета Пользователя'

    @property # используется для создания <<специальной>> функциональности определеным методам
    def get_course_sum(self):
        """Получение полной суммы счета с учетом курса валют"""
        sum = self.sum
        course = self.course
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
        on_delete=models.CASCADE, 
        verbose_name='Категория'
    )
    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name='Счет'
    )
    created_at = models.DateField(
        auto_now=True, 
        verbose_name='Дата'
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
        return f'Категория: pk={self.pk}, category={self.category}, parent={self.parent}, sum={self.sum}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Расход пользователя'
        verbose_name_plural = 'Расходы пользователей'

    @property # используется для создания <<специальной>> функциональности определеным методам
    def get_total_price(self):
        """Для получения суммы Расходов"""
        expenses = UserExpenses.objects.all()
        total_price = sum(
            [expense.sum for expense in expenses]
        )
        return total_price

class UserIncomes(models.Model):
    """Доходы пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        verbose_name='Пользователь'
    )
    category = models.ForeignKey(
        CategoryIncome,
        on_delete=models.CASCADE, 
        verbose_name='Категория'
    )
    account = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        verbose_name='Счет'
    )
    created_at = models.DateField(
        auto_now=True, 
        verbose_name='Дата'
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
        return f'Категория: pk={self.pk}, category={self.category}, parent={self.parent}, sum={self.sum}'
    
    class Meta:
        """Характер Класса"""
        verbose_name = 'Доходы пользователя'
        verbose_name_plural = 'Доходы пользователей'
    
    @property # используется для создания <<специальной>> функциональности определеным методам
    def get_total_price(self):
        """Для получения суммы доходов"""
        incomes = UserIncomes.objects.all()
        total_price = sum(
            [income.sum for income in incomes]
        )
        return total_price



