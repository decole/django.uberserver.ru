from django.core.mail import send_mail


def send_email(title, message, address):
    send_mail(
        title,
        message,
        'noreply@uberserver.ru',
        address,  # ['to@example.com'],
        fail_silently=False,
    )
