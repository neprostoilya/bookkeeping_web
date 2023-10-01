from django.conf import settings

from conf.celery import app

from .service import send_activate_email_message


@app.task
def send_activate_email_message_task(user_id):
    """Отправка письма подтверждения осуществляется через функцию: send_activate_email_message"""
    return send_activate_email_message(user_id)

