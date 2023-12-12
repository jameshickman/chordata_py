"""
Email sending utilities
"""


def send_email(
        configuration: dict,
        address_from: str,
        address_to: str,
        subject: str,
        message_text: str,
        message_html: str = '',
        attachments: list = []
):
    import smtplib
    import ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = address_from
    message["To"] = address_to
    part1 = MIMEText(message_text, "plain")
    message.attach(part1)
    for attachment in attachments:
        att = load_attachment(
            attachment['src'],
            attachment['name'],
            attachment['mime']
        )
        if att is not False:
            message.attach(att)
    if configuration['email_secured'] == 'True':
        context = ssl.create_default_context()
    with smtplib.SMTP(configuration['email_host'], int(configuration['email_port'])) as server:
        if configuration['email_secured'] == 'True':
            server.starttls(context=context)
            server.login(configuration['email_user'], configuration['email_password'])
        server.sendmail(address_from, address_to, message.as_string())
    return True


def load_attachment(src_filename: str, filename: str, mime: str = "application"):
    from email import encoders
    from email.mime.base import MIMEBase
    try:
        with open(src_filename, "rb") as attachment:
            part = MIMEBase(mime, "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}".format(filename=filename)
            )
            return part
    except FileNotFoundError as e:
        return False
