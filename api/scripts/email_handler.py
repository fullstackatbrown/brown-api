import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

URGENT_RECEPIENT = "7172159174@vtext.com"
ALERT_RECEPIENT = "fullstack@brown.edu"


def send_id_email(address, name, client_id):
    # me == my email address
    # you == recipient's email address
    me = os.environ['GMAIL_USER']

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your Brown APIs Client ID"
    msg['From'] = me
    msg['To'] = address

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi, " + name + "! Welcome to the Brown APIs developer community.\nYour Client ID is: " + client_id
    html = """\
    <html>
      <head>
            <style>
                    p {
                        font-size: 14px;
                    }
                    .center {
                            margin: auto;
                            text-align: center;
                    }
            </style>
      </head>
      <body>
        <h2 class="center">Hi, """ + name + """! Welcome to the Brown APIs developer community.</h2>
        <p>Your Client ID is: <em>""" + client_id + """</em>.</p>
        <p>Be sure to include your Client ID with every request you make! You can use this Client ID for multiple projects. Currently, there is a maximum of one Client ID per student, but exceptions can be made on a case-by-case basis.</p>
        <p>Brown APIs are currently in beta. This means functionality may be added, removed, or modified at any time (however, this is very rare). To keep up-to-date on any changes, be sure to join our <a href="https://www.facebook.com/groups/brown.apis/">community of developers</a> on Facebook.</p>
        <br />
        Happy developing! <br />
        The Brown APIs Team
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASS'])

    try:
        print(s.sendmail(me, address, msg.as_string()))
    except:
        s.quit()
    s.quit()

def send_alert_email(message, urgent=False):
    # me == my email address
    me = os.environ['GMAIL_USER']
    # recepient's email address depends on how urgent the alert is
    recepient = URGENT_RECEPIENT if urgent else ALERT_RECEPIENT

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Brown APIs - Urgent Alert!" if urgent else "Brown APIs - System Error"
    msg['From'] = me
    msg['To'] = recepient

    # Create the body of the message (a plain-text and an HTML version).
    text = message
    html = """\
    <html>
      <head>
            <style>
                    p {
                        font-size: 14px;
                    }
                    .center {
                            margin: auto;
                            text-align: center;
                    }
            </style>
      </head>
      <body>
            <p><em>The following message was generated moments ago on the Brown APIs server:</em></p>
        <p>""" + message + """</p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(os.environ['GMAIL_USER'], os.environ['GMAIL_PASS'])

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    print(s.sendmail(me, recepient, msg.as_string()))
    s.quit()
