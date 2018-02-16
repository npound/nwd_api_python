
import sendgrid
import os
from sendgrid.helpers.mail import *
from nwd_config import NWD_CONGIG
from nwd_db import NWD_DB, uuid, os

class NWD_SENDGRID:

  def send_password_reset(self, email):
    config = NWD_CONGIG()
    db = NWD_DB()
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("PasswordReset@NWD.com")
    to_email = Email(email)
    subject = "Password Reset Request"

    password_reset_string = (uuid.uuid4().hex+uuid.uuid4().hex)

    content = Content("text/plain","A password reset has been requested. Please follow this link to reset your password.\n "+config.host+"/PasswordReset/"+password_reset_string)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


    print(response.status_code)
    db.init_password_reset(email,password_reset_string)