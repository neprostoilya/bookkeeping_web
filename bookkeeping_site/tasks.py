from conf.celery import app

from .service import send_activate_email_message, render_graphic_account, \
    render_graphic_expenses, render_graphic_incomes

@app.task
def send_activate_email_message_task(user_id):
    """Отправка письма подтверждения осуществляется через функцию: send_activate_email_message"""
    return send_activate_email_message(user_id)

@app.task
def render_graphic_account_task(user):
    """Рендеринг графика счетов осуществляется через функцию: render_graphic_account"""
    return render_graphic_account(user)

@app.task
def render_graphic_incomes_task(user, year, month):
    """Рендеринг графика доходов осуществляется через функцию: render_graphic_incomes"""
    return render_graphic_incomes(user, year, month)

@app.task
def render_graphic_expenses_task(user, year, month):
    """Рендеринг графика расходов осуществляется через функцию: render_graphic_expenses"""
    return render_graphic_expenses(user, year, month)