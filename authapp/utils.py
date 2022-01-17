from django.core.mail import send_mail
from django.urls import reverse
from geekshop import settings


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Activation email'

    message = f'To confirm your account {user.username} on \
    {settings.DOMAIN_NAME} please, follow the link: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)