from passlib.context import CryptContext
from passlib.hash import argon2
from passlib.exc import UnknownHashError
import secrets
import logging
import smtplib
import ssl
from gourmandapiapp.config import settings
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

env_context = Environment(loader=FileSystemLoader('./gourmandapiapp/templates'))
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

def send_mail(email: str, subject, **kwargs):
    from_email = settings.SMTP_USER
    email_prefix = from_email.split('@')[0]
    if email.split('@')[0].split('+')[0] != email_prefix:
        return None
    context_ssl = ssl.create_default_context()
    mssg_transformed = MIMEMultipart('alternative')
    mssg_transformed.add_header('from', settings.SMTP_USER)
    mssg_transformed.add_header('to', email)
    mssg_transformed.add_header('subject', subject)

    template_rendered_txt = render_template(template='auth_email_confirm.txt', **kwargs)
    part1 = MIMEText(template_rendered_txt, 'plain')
    template_rendered_html = render_template(template='auth_email_confirm.html', **kwargs)
    part2 = MIMEText(template_rendered_html, 'html')

    mssg_transformed.attach(part1)
    mssg_transformed.attach(part2)

    with smtplib.SMTP(host=settings.SMTP_SERVER, port=settings.SMTP_PORT,) as server:
        server.ehlo()
        server.starttls(context=context_ssl) # refactor to use implicit TLS
        server.ehlo()
        server.login(user=settings.SMTP_USER, password=settings.SMTP_KEY)
        server.sendmail(
            from_addr=settings.SMTP_USER,
            to_addrs=email,
            msg=mssg_transformed.as_string()
        )
    logging.info(msg=f"Sending {mssg_transformed.as_string()} to \n {email}")

def render_template(template, **kwargs):
    # env_context.get_template('auth_email_confirm.html')
    template_retrieved = env_context.get_template(template)
    template_rendered = template_retrieved.render(**kwargs)
    return template_rendered

# def construct_email_message(**kwargs):
#     mssg_transformed = MIMEMultipart('alternative')
#     mssg_transformed.add_header('from', settings.SMTP_USER)
#     mssg_transformed.add_header('to', email)
#     mssg_transformed.add_header('subject', subject)
#     mssg_transformed.set_payload(mssg)
#     render_template()
