import json
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import pytz
import requests

today_date = (datetime.now(pytz.utc) - timedelta(days=1)).replace(hour=18, minute=30, second=0, microsecond=0).strftime(
    "%Y-%m-%dT%H:%M:%S.000Z") # keep days-1 always in UTC its send at days-1 time

def test_cms_listing_created_by():
    url = f"https://cms.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=createdAt:ASC&filters[$and][0][createdAt][$gt]={today_date}"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImlhdCI6MTcxMDg2NjMwMywiZXhwIjoxNzEzNDU4MzAzfQ.dEKeQmWvgG3QGwCFuhXFppEdrfE7II9uSWU7mwXMIMQ',
        'Connection': 'keep-alive',
        'Cookie': '_clck=1l4b3wp%7C2%7Cfio%7C0%7C1484; _ga=GA1.2.187986154.1706094271; _ga_G6WKMM3SPZ=GS1.1.1706094271.1.1.1706094324.7.0.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    total=json_response["pagination"]["total"]
    createdAt = json_response["results"][0]["createdAt"]
    org_name = json_response["results"][0]["organisation"]["name"]
    # print("\n Today's Total Count of file is " + str(createdAt))
    print("\n Org name is  " + str(org_name))

    IST = pytz.timezone('Asia/Kolkata')
    createdAt_ist = datetime.strptime(createdAt, '%Y-%m-%dT%H:%M:%S.%fZ').replace(
        tzinfo=pytz.utc).astimezone(IST)
    createdAt_cal = createdAt_ist.strftime('%Y-%m-%d %H:%M:%S')
    print(createdAt_cal)
    global createdAt_final
    createdAt_final=createdAt_cal
    global org_final
    org_final = org_name
    global total_final
    total_final=total

def test_cms_listing_success():
    url = f"https://cms.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:ASC&filters[$and][0][createdAt][$gt]={today_date}&filters[$and][1][status][$eq]=success"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImlhdCI6MTcxMDg2NjMwMywiZXhwIjoxNzEzNDU4MzAzfQ.dEKeQmWvgG3QGwCFuhXFppEdrfE7II9uSWU7mwXMIMQ',
        'Connection': 'keep-alive',
        'Cookie': '_clck=1l4b3wp%7C2%7Cfio%7C0%7C1484; _ga=GA1.2.187986154.1706094271; _ga_G6WKMM3SPZ=GS1.1.1706094271.1.1.1706094324.7.0.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    success_total=json_response["pagination"]["total"]
    print("\n Org name is  " + str(success_total))
    global success_final
    success_final=success_total


def test_cms_listing_updated_by():
    url = f"https://cms.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=updatedAt:DESC&filters[$and][0][createdAt][$gt]={today_date}"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImlhdCI6MTcxMDg2NjMwMywiZXhwIjoxNzEzNDU4MzAzfQ.dEKeQmWvgG3QGwCFuhXFppEdrfE7II9uSWU7mwXMIMQ',
        'Connection': 'keep-alive',
        'Cookie': '_clck=1l4b3wp%7C2%7Cfio%7C0%7C1484; _ga=GA1.2.187986154.1706094271; _ga_G6WKMM3SPZ=GS1.1.1706094271.1.1.1706094324.7.0.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    updatedAt = json_response["results"][0]["updatedAt"]
    # print("\n updated " + str(updatedAt))
    IST = pytz.timezone('Asia/Kolkata')
    updatedAt_ist = datetime.strptime(updatedAt, '%Y-%m-%dT%H:%M:%S.%fZ').replace(
        tzinfo=pytz.utc).astimezone(IST)
    updatedAt_cal = updatedAt_ist.strftime('%Y-%m-%d %H:%M:%S')
    print(updatedAt_cal)
    global updatedAt_final
    updatedAt_final=updatedAt_cal


def test_calculate_processing_time():
    created_at = datetime.strptime(createdAt_final, '%Y-%m-%d %H:%M:%S')
    updated_at = datetime.strptime(updatedAt_final, '%Y-%m-%d %H:%M:%S')

    time_difference = updated_at - created_at
    hours, remainder = divmod(time_difference.total_seconds(), 3600)
    minutes = remainder // 60
    proccesing_time = f"{int(hours)} hours, {int(minutes)} minutes"
    print(proccesing_time)
    global proccesing_time_final
    proccesing_time_final=proccesing_time

def test_send_mail():
    # AWS SMTP credentials
    smtp_username = 'AKIA5YBB6OJ66G2MXV7B'
    smtp_password = 'BMX8OsOi7Gy4OLgEsaKvyICJQbDOYv8XVEHtE2DGcLIE'
    smtp_hostname = 'email-smtp.eu-west-1.amazonaws.com'
    smtp_port = 587  # Adjust the port if necessary

    # Sender and recipient email addresses
    sender_email = 'no-reply@mail.englishscore.com'
    # Recipient email address
    #recipient_emails = ["susmit.surwade@blenheimchalcot.com"]
    recipient_emails = ["susmit.surwade@blenheimchalcot.com","satyendra.kumar@blenheimchalcot.com","lokesh.singh@blenheimchalcot.com","rinkesh.das@blenheimchalcot.com","ami.jambusaria@blenheimchalcot.com","aashish.paruvada@blenheimchalcot.com"]

    # Variables with total count and success count
    org_mail= org_final
    created_at_mail = createdAt_final
    updated_at_mail = updatedAt_final
    processing_mail=proccesing_time_final
    succes_mail=success_final


    # Create message container
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Brocaly Support', sender_email))
    msg['To'] = ', '.join(recipient_emails)
    yesterday_date=(datetime.now() - timedelta(days=0)).strftime('%d-%m-%Y')
    msg['Subject'] = f"Daily Report: File Processing time for Date - {yesterday_date}"

    # body = f" Files received in CMS today as below: \n Organisation: Oakbrook \n Total Count: {total_count}\n Success Count: {success_count}\n Failed Count: {failed_count}\n Transcribed Count: {transcribed_count} "
    body = f"""
        <html>
          <body>
            <table border="1">
                <tr>
                    <td>Organisation:</td>
                    <td style="text-align: center;">{org_final}</td>
                </tr>
                <tr>
                    <td>Total Files Received In Cms:</td>
                    <td style="text-align: center;">{total_final}</td>
                </tr>
                  <tr>
                    <td>Total Files Processed:</td>
                    <td style="text-align: center;">{succes_mail}</td>
                </tr>
                <tr>
                    <td>First Created At</td>
                    <td style="text-align: center;">{created_at_mail}</td>
                </tr>
                <tr>
                    <td>Last Updated At:</td>
                    <td style="text-align: center;">{updated_at_mail}</td>
                </tr>
                <tr>
                    <td>Total processing time</td>
                    <td style="text-align: center;">{processing_mail}</td>
                </tr>   
            </table>
          </body>
        </html>
        """

    # Attach body to the email
    msg.attach(MIMEText(body, 'html'))

    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_hostname, smtp_port)
        server.starttls()

        # Login with your SMTP credentials
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_emails, msg.as_string())

        print('Email sent successfully!')

    except Exception as e:
        print('Error: Unable to send email.')
        print(e)

    finally:
        # Close the SMTP server connection
        server.quit()
