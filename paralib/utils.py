from email.message import EmailMessage
from email.mime.text import MIMEText
from typing import Sequence
from aiosmtplib import SMTP
from pydantic import EmailStr

from db.curd import get_config_by_key


async def send_mail(to_mails: Sequence[EmailStr], text: str, subject: str, email_type: str):
    """
    发送邮件
    :param to_mails:
    :param text:
    :param subject:
    :param email_type:
    :return:
    """
    to_mails = to_mails
    text = text
    subject = subject
    config = await get_config_by_key('email_config')
    client = SMTP(hostname=config.get('mail_host'), port=config.get('mail_port'), username=config.get('mail_user'),
                  password=config.get('mail_password'), use_tls=True)
    if email_type == "html":
        message = MIMEText(text, 'html', 'utf-8')
    else:
        message = EmailMessage()
        message.set_content(text)
    message['From'] = config.get('mail_send_from')
    message['Subject'] = subject
    async with client:
        ret = await client.send_message(message, recipients=to_mails)
    return ret
