import smtplib
from email.mime.application import MIMEApplication

import pytz
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
    report_file_path = "allure-report/index.html"
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