from django.contrib.auth.tokens import default_token_generator
from api_yamdb.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Токен для авторизации YaMDb'
    message = f'{confirmation_code} - ваш код для авторизации на YaMDb'
    admin_email = EMAIL_HOST_USER
    user_email = [user.email]
    send_mail(subject, message, admin_email, user_email)
