import os
import smtplib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class NotificationManager:
    # TODO: Send SMS message to WhatsApp instead of email.

    def __init__(self, price, departure, arrival, out_date):
        """
        Constructor to create a message and send it via smtp.gmail.com

        :param price: minimum price found
        :param departure: date of departure
        :param arrival: iata code of the airport
        :param out_date: date of return
        """
        self._mail =os.environ.get("MAIL_ADDRESS")
        self._passwd =os.environ.get("MAIL_PASSWD")
        self.price = price
        self.departure = departure
        self.arrival = arrival
        self.out_date = out_date

    def create_msg(self):
        """
        Create a message to send

        :return: formatted message as str
        """

        msg = f"Price: {self.price}\nDeparture Airport IATA Code: {self.departure}\nArrival Airport IATA Code: {self.arrival}\nOutbound Date: {self.out_date}\n"
        #msg_utf8 = msg.encode("utf-8") # This is not necessary
        return msg

    def send_mail(self):
        """
        Send the formatted to message to gmail.

        :return: None
        """

        msg = self.create_msg()
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(self._mail, self._passwd)
            smtp.sendmail(
                from_addr=self._mail,
                to_addrs=self._mail,
                msg=f"Subject: Cheapest Flight\n\n{msg}")