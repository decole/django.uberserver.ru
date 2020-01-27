from django.core.mail import send_mail


# Хелпер для работы с отправкой писем
def send_email(title, message, address):
    if isinstance(address, list):
        return __sender(title, message, address)

    if isinstance(address, str):
        return __sender(title, message, [address])


def __sender(title, message, address):
    send_mail(
        subject='Notification Uberserver.ru - ' + title,
        message=message,
        from_email='decole2014@yandex.ru',
        recipient_list=address,
        fail_silently=False
    )

