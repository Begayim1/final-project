from  django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import CustomUser


def send_activation_code(email, activation_code, status):
    if status == 'register':
        context = {
            'text_detail': "Thank you for registration!",
            "email": email,
            "domain": "http://localhost:8000",
            "activation_code": activation_code
        }

        msg_html = render_to_string('email.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Activate Your Account',
            message,
            'stackoverflow_admin@gmail.com',
            [email, ],
            html_message=msg_html,
            fail_silently=False
        )
    elif status == 'reset_password':
        send_mail(
            'Reset Your password',
            f'Ков активации: {activation_code}',
            'bookblog_admin@gmail.com',
            [email, ],
            fail_silently=False
        )