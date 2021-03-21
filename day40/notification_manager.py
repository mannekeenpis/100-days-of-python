import smtplib
from twilio.rest import Client

TWILIO_SID = YOUR TWILIO ACCOUNT SID
TWILIO_AUTH_TOKEN = YOUR TWILIO AUTH TOKEN
TWILIO_VIRTUAL_NUMBER = YOUR TWILIO VIRTUAL NUMBER
TWILIO_VERIFIED_NUMBER = YOUR TWILIO VERIFIED NUMBER
MAIL_PROVIDER_SMTP_ADDRESS = YOUR EMAIL PROVIDER SMTP ADDRESS "smtp.gmail.com"
MY_EMAIL = YOUR EMAIL
MY_PASSWORD = YOUR PASSWORD

class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        print(message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP(MAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )