#! /usr/bin/python

import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    '''
    This function sends a email with attachments

    :param str send_from: The send-from address
    :param list send_to: A list of email addresses to send to
    :param str subject: The subject of the email
    :param str text: The body of the email
    :param list files: A list of filenames to attach
    :param str server: The domain of the SMTP Server
    '''
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP_SSL(server, 443)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

if __name__=="__main__":
    send_mail('matt@freelancer.com', ['stephen@tridgell.net'], 'AutoTest Results', '', [], 'mail.iinet.net.au')
