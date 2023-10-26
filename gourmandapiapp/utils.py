from passlib.context import CryptContext
from passlib.hash import argon2
from passlib.exc import UnknownHashError
import secrets
import logging
import smtplib
import ssl
from gourmandapiapp.config import settings
from email import message

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

interface_argon2 = lambda the_salt: argon2.using(salt_size=16, rounds=2, salt=the_salt)

def get_password_hash(password):
    # TODO: encode in UTF8 bytes
    salt = secrets.token_bytes(16)
    return  interface_argon2(the_salt=salt).hash(password)

def verification(plain_password, hashed_password):
    salt = secrets.token_bytes(16)
    for algo in [interface_argon2(the_salt=salt), pwd_context]:
        try:
            if algo.verify(plain_password,hashed_password):
                return True
        except (UnknownHashError, ValueError) as ex:
            print(f'{ex}:Reverting to bcrypt algo')
            continue
    return False

def send_mail(email, subject, mssg):
    context_ssl = ssl.create_default_context()
    mssg_transformed = message.Message()
    mssg_transformed.add_header('from', settings.SMTP_USER)
    mssg_transformed.add_header('to', email)
    mssg_transformed.add_header('subject', subject)
    mssg_transformed.set_payload(mssg)
    with smtplib.SMTP(host=settings.SMTP_SERVER, port=settings.SMTP_PORT,) as server:
        server.ehlo()
        server.starttls(context=context_ssl)
        server.ehlo()
        server.login(user=settings.SMTP_USER, password=settings.SMTP_KEY)
        server.sendmail(
            from_addr=settings.SMTP_USER,
            to_addrs=email,
            # msg=bytes(mssg, encoding='utf8')
            msg=mssg_transformed.as_string()
        )
    logging.info(msg=f"Sending {mssg} to \n {email}")