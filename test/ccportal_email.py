import smtplib
from email.mime.application import MIMEApplication
import pytest
import pytz
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import shutil
import zipfile


"""
def test_send_mail():
    # Your email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "susmit.s.surwade@gmail.com"
    smtp_password = "qzod ltfm nmav tqvw"

    # Recipient email address
    recipient_emails = ["susmit.surwade@blenheimchalcot.com"]
    #recipient_emails = ["susmit.surwade@blenheimchalcot.com", "lokesh.singh@blenheimchalcot.com", "ruksar.khan@blenheimchalcot.com","ami.jambusaria@blenheimchalcot.com"]

    # Format today's date
    #today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S")

    # Create the email message
    subject = f"Daily Test Automation Report: {today_date}"
    body = f"Please find Attached Test Automation Report"

    message = MIMEMultipart()
    message["From"] = smtp_username
    # message["To"] = recipient_email
    message['To'] = ', '.join(recipient_emails)
    message["Subject"] = subject
    #message.attach(MIMEText(body, "plain"))

    # Read the HTML report file
    report_file_path = "test/reports"
    with open(report_file_path, "rb") as report_file:
        report_attachment = MIMEApplication(report_file.read(), _subtype="html")
        report_attachment.add_header("Content-Disposition", "attachment", filename="index.html")
        message.attach(report_attachment)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        # server.sendmail(smtp_username, recipient_email, message.as_string())
        for recipient_email in recipient_emails:
            server.sendmail(smtp_username, recipient_email, message.as_string())
    print("\n Email sent successfully.")
"""

def send_email():
        # Email details
        today_date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S")
        recipient_emails = ["susmit.surwade@blenheimchalcot.com"]
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = "susmit.s.surwade@gmail.com"
        smtp_password = "qzod ltfm nmav tqvw"
        receiver_email = "susmit.surwade@blenheimchalcot.com"
        subject = f"CC DAILY AUTOMATION REPORT: {today_date}"
        body = "Please find the attached report zip file , you need to download and view the html report."

        # Folder paths
        report_folder = r"allure-report"
        attachment_path = r"allure-report\index.html"

        # Create ZIP file
        with zipfile.ZipFile(attachment_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Traverse the directory tree and add files to the ZIP file
            for root, dirs, files in os.walk(report_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, report_folder)
                    zipf.write(file_path, relative_path)

        # Create email message
        message = MIMEMultipart()
        message["From"] = smtp_username
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Attach ZIP file
        filename = os.path.basename(attachment_path)
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            message.attach(part)

        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            # server.sendmail(smtp_username, recipient_email, message.as_string())
            for recipient_email in recipient_emails:
                server.sendmail(smtp_username, recipient_email, message.as_string())
        print("\n Email sent successfully.")

        # Cleanup: Delete the ZIP file after sending email
        os.remove(attachment_path)

    # Example usage
def test_send_email():
    send_email()
