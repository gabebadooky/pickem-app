from dotenv import load_dotenv
from email.message import EmailMessage
import os, smtplib

load_dotenv()

def create(to: str, user_id: int, endpoint_name: str, body: str) -> EmailMessage:
    """Method that instantiates the Email Message object with the inputted parameters"""
    msg = EmailMessage()
    msg["From"] = "no-reply@have-a-nice-pickem.com"
    msg["To"] = to
    msg["Subject"] = f"Error occurred for USER_ID {user_id} at /{endpoint_name} endpoint!"
    msg.set_content(body)
    return msg


def send(msg: EmailMessage):
    """Method that accepts and sends an EmailMessage object"""
    s: smtplib.SMTP = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("gb.pickem@gmail.com", os.getenv("GMAIL_PASSWORD"))
    #s.send_message(msg)
    #s.sendmail("gb.pickem@gmil.com", "gb.pickem@gmil.com", msg.get_content())
    s.send_message(create())


send(create("baduquig@gmail.com", 1, "/test", "ERR"))