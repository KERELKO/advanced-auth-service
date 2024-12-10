from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from aiosmtplib.errors import SMTPException
from loguru import logger

from .interfaces import AbstractNotificationService


class DummyNotificationService(AbstractNotificationService):
    async def send(self, message: str, subject: str, to: str) -> None:
        print(message, subject, to)


class EmailNotificationService(AbstractNotificationService):
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        email_address: str,
        email_password: str,
    ) -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.__email_password = email_password

    async def send(self, message: str, subject: str, to: str) -> None:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            await aiosmtplib.send(
                msg,
                hostname=self.smtp_server,
                port=self.smtp_port,
                start_tls=True,
                username=self.email_address,
                password=self.__email_password,
            )

            logger.info(f'Sended email to {subject}')
        except SMTPException as e:
            logger.error(e)
