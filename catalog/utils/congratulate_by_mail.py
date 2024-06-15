import os
import smtplib
from email.mime.text import MIMEText

from config import settings


def congratulate_by_mail(blogpost):
    if blogpost.views_count == 100:
        subject = 'Поздравляем, вы достигли отметки в 100 просмотров!'
        body = f'Ваш пост "{blogpost.title}" был просмотрен 100 раз!'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = settings.EMAIL_RECIPIENT

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            smtp.send_message(msg)
            print(f'Письмо отправлено на {settings.EMAIL_RECIPIENT}')
