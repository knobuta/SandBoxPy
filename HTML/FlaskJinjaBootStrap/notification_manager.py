import os
import smtplib

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class NotificationManager:
    # TODO: Send SMS message to WhatsApp instead of email.

    def __init__(self, name, email, phone, message):
        """
        Constructor to create a message and send it via smtp.gmail.com
        """
        self._mail =os.environ.get("MAIL_ADDRESS")
        self._passwd =os.environ.get("MAIL_PASSWD")
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message

    def create_msg(self):
        """
        Create a message to send

        :return: formatted message as str
        """

        msg = f"Name: {self.name}\nEmail: {self.email}\nPhone: {self.phone}\nMessage: {self.message}\n"
        # msg_utf8 = msg.encode("utf-8") # This is not necessary
        return msg

    def send_mail(self):
        """
        Send the formatted to message to gmail.

        :return: None
        """

        msg = self.create_msg()
        with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login(self._mail, self._passwd)
            smtp.sendmail(
                from_addr=self._mail,
                to_addrs=self._mail,
                msg=f"Subject: Blog\n\n{msg}")