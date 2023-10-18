
import smtplib

def SMTP_send_email(recipient, subject, body):
  """Sends an email from the sender to the recipient.

  Args:
    recipient: The email address of the recipient.
    subject: The subject of the email.
    body: The body of the email.
  """

  # Create an SMTP object.
  smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  sender = 'freshkeeper.contact@gmail.com'
  # Login to the SMTP server.
  smtp_server.login(sender, 'fkgu twdc wzjt oyeb')

  # Create an email message.
  message = """From: {}
To: {}
Subject: {}

{}
""".format(sender, recipient, subject, body)

  # Send the email message.
  smtp_server.sendmail(sender, recipient, message)

  # Close the SMTP connection.
  smtp_server.quit()