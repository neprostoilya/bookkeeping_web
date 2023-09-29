from celery import shared_task
from django.core.mail import send_mail

from conf import settings

from .models import User
from .service import generate_activation_code

@shared_task
def send_activation_code(request, user_id):
    user = User.objects.get(id=user_id)
    code = generate_activation_code()
    send_mail(
        subject='Бухгалтерия',
        message=code,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
    request.session['activation_code'] = code
    request.save()