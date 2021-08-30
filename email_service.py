import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List


def send_email(sender_address: str, sender_pass: str, to_mail: str, mail_content: str, subject: str,
               file_paths: List[str] = None, file_names: List[str] = None) -> dict:
    """
    This is a simple function for sending email with file attachment option also.
    @author: andy
    @sender_address: email_address for the sender
    @sender_pass: password of sender_address
    @param to_mail: the recipient's email-id
    @param mail_content: The body of email
    @param subject: Subject of the mail
    @param file_path: list of file paths that may be attached with the email
    @param file_name: the list of file names
    @return:
    """
    print("Sending mail to {}".format(to_mail))
    message = MIMEMultipart()
    message["From"] = sender_address
    message['To'] = to_mail
    message['Subject'] = subject
    message.attach(MIMEText(mail_content, 'plain'))
    if file_paths is not None:
        for file_path, file_name in zip(file_paths, file_names):
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file_path, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={}'.format(file_name))
            message.attach(part)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, to_mail, text)
    session.quit()
    return {"status_code": 200, "message": "The mail has been sent successfully to {}".format(to_mail)}

