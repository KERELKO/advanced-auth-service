from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from aiosmtplib.errors import SMTPException
from loguru import logger

from src.core.config import Config

from .interfaces import AbstractNotificationService


class EmailNotificationService(AbstractNotificationService):
    def __init__(
        self,
        config: Config,
    ) -> None:
        self.smtp_server = config.smtp_server
        self.smtp_port = config.smtp_port
        self.email_address = config.email_address
        self.__email_password = config.email_password

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

            logger.info(f'Sent email: subject={subject}, to={to}')
        except SMTPException as e:
            logger.error(f'Failed to send email: {e}')
