from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time
import datetime


# @shared_task
# def add(x, y):
#     print(f"args {x} and {y}")
#     return x + y


# @shared_task
# def send_otp(email, code):
#     send_mail(
#         "OTP code",
#         f"your code {code}",
#         settings.EMAIL_HOST_USER,
#         [email],
#         fail_silently=False,
#     )
    
# @shared_task
# def send_report():
#     send_mail(
#         "Report",
#         "Что то ооооочень важное",
#         settings.EMAIL_HOST_USER,
#         ["riszav.01@gmail.com"],
#         fail_silently=False,
#     )

@shared_task
def long_running_task(n):
    time.sleep(n)
    return f"Задача завершилась за {n} секунд"

@shared_task
def print_hello():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] Привет из Celery!")

@shared_task
def send_welcome_email(to_email):
    send_mail(
        subject="Добро пожаловать!",
        message="Спасибо за регистрацию!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return f"Письмо отправлено на {to_email}"