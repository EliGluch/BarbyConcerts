import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mail:

    def get_mail_config():
        '''Gets email address and password from file'''
        with open('mail.config', "r") as json_file:
            configDict = json.load(json_file)

            return configDict

    def send_email(destinations=None, subject='', body='', attachments=None):
        configDict = Mail.get_mail_config()

        gmail_user        = configDict['user']
        gmail_password    = configDict['password']
        sent_from         = gmail_user
        destinations      = destinations if destinations else [configDict['dest']]
        destinations_text = ", ".join(destinations)

        msg            = MIMEText(body, _charset="UTF-8")
        msg['Subject'] = subject
        msg['From']    = gmail_user
        msg['To']      = destinations_text

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, destinations, msg.as_string())

        except:
            print ('Something went wrong...')

        finally:
            server.close()
