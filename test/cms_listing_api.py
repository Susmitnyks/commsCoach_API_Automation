import json
import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

current_date = datetime.now()
yesterday_date = current_date - timedelta(days=2)
formatted_yesterday = yesterday_date.strftime("%Y-%m-%d")
date = formatted_yesterday + "T18:30:00.000Z"



def test_count_success():
    global SCount
    url = "https://cms-stage.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=organisation[name]:DESC&filters[$and][0][createdAt][$gt]="+date+"&filters[$and][1][status][$eq]=success"
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImlhdCI6MTcwNjcwMzc5NSwiZXhwIjoxNzA5Mjk1Nzk1fQ.5rxDXnOloAGiXF5SRDVZO8E3UN1jtOHpCiD_Nsd-lFE'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    SCount = json_response["pagination"]["total"]
    print("\n Today's Success Count is " + str(SCount))


def test_count_total():
    global TCount
    url = "https://cms-stage.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=organisation[name]:DESC&filters[$and][0][createdAt][$gt]="+date+""
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImlhdCI6MTcwNjcwMzc5NSwiZXhwIjoxNzA5Mjk1Nzk1fQ.5rxDXnOloAGiXF5SRDVZO8E3UN1jtOHpCiD_Nsd-lFE'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    TCount = json_response["pagination"]["total"]
    print("\n Today's Total Count is " + str(TCount))


def test_count_fail():
    global FCount
    url = "https://cms-stage.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=organisation[name]:DESC&filters[$and][0][createdAt][$gt]="+date+"&filters[$and][1][status][$eq]=failed"
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImlhdCI6MTcwNjcwMzc5NSwiZXhwIjoxNzA5Mjk1Nzk1fQ.5rxDXnOloAGiXF5SRDVZO8E3UN1jtOHpCiD_Nsd-lFE'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    FCount = json_response["pagination"]["total"]
    print("\n Today's Failed Count is " + str(FCount))

def test_count_transcribed():
    global TRCount
    url = "https://cms-stage.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=organisation[name]:DESC&filters[$and][0][createdAt][$gt]=" + date + "&filters[$and][1][status][$eq]=transcribed"
    payload = {}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImlhdCI6MTcwNjcwMzc5NSwiZXhwIjoxNzA5Mjk1Nzk1fQ.5rxDXnOloAGiXF5SRDVZO8E3UN1jtOHpCiD_Nsd-lFE'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    TRCount = json_response["pagination"]["total"]
    print("\n Today's Transcribed Count is " + str(TRCount))


def test_send_mail():
    # Your email configuration


    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "automationsreport@gmail.com"
    smtp_password ="ixwe pwrz xprs adwf"
    #"qzod ltfm nmav tqvw"

    # Recipient email address
    recipient_emails = "susmit.surwade@blenheimchalcot.com"
    #recipient_emails=["susmit.surwade@blenheimchalcot.com", "susmit.s.surwade@gmail.com"]

    # Variables with total count and success count
    total_count = TCount
    success_count = SCount
    failed_count=FCount
    transcribed_count=TRCount

    # Format today's date
    today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the email message
    subject = f"Today's File Count - {today_date}"
    #body = f" Files received in CMS today as below: \n Organisation: Oakbrook \n Total Count: {total_count}\n Success Count: {success_count}\n Failed Count: {failed_count}\n Transcribed Count: {transcribed_count} "
    body = f"""
    <html>
      <body>
        <p><b>Files received in CMS today as below:</b></p>
        <ul>
          <li>Organisation: Oakbrook</li>
          <li>Total Count: {total_count}</li>
          <li>Success Count: {success_count}</li>
          <li>Failed Count: {failed_count}</li>
          <li>Transcribed Count: {transcribed_count}</li>
        </ul>
      </body>
    </html>
    """
    message = MIMEMultipart()
    message["From"] = smtp_username
    #message["To"] = recipient_email
    message['To'] = ', '.join(recipient_emails)
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
       server.starttls()
       server.login(smtp_username, smtp_password)
       #server.sendmail(smtp_username, recipient_email, message.as_string())
       for recipient_email in recipient_emails:
           server.sendmail(smtp_username, recipient_email, message.as_string())

    print("Email sent successfully.")