import json
import smtplib
from email.utils import formataddr
import pytest
import requests
import pytz
from datetime import datetime, timedelta, timezone
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from azure.storage.blob import BlobServiceClient

today_date_mail = (datetime.now(pytz.timezone('Asia/Kolkata')) - timedelta(days=0)).strftime("%d-%m-%Y %H:%M:%S")  # Keep today's Day before date ie day=0
today_date = (datetime.now(pytz.utc) - timedelta(days=2)).replace(hour=18, minute=30, second=0, microsecond=0).strftime(
    "%Y-%m-%dT%H:%M:%S.000Z") # keep days-1 always in UTC its send at days-1 time

# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5NjI5NzU5NmJiNWQ4N2NjOTc2Y2E2YmY0Mzc3NGE3YWE5OTMxMjkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3VzbWl0IFN1cndhZGUiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXMtYWktYXV0aCIsImF1ZCI6ImVzLWFpLWF1dGgiLCJhdXRoX3RpbWUiOjE3MDY4ODI5NTYsInVzZXJfaWQiOiJXQUc4NVhpbXlSY0ZnOFRwa21Hbk9FSWtBTUIzIiwic3ViIjoiV0FHODVYaW15UmNGZzhUcGttR25PRUlrQU1CMyIsImlhdCI6MTcwNzA3NDMyNCwiZXhwIjoxNzA3MDc3OTI0LCJlbWFpbCI6InN1c21pdC5zdXJ3YWRlQGJsZW5oZWltY2hhbGNvdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsibWljcm9zb2Z0LmNvbSI6WyI2ZTNiNTcxNy1kZTNlLTRmNGYtYjBlOC02ODc3MzBiNjE3YjUiXSwiZW1haWwiOlsic3VzbWl0LnN1cndhZGVAYmxlbmhlaW1jaGFsY290LmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Im1pY3Jvc29mdC5jb20ifX0.k32njBhaAYv0zM6vSXIcxEVqXsQSja4bbd4PM2I5bChb1kvJjCa9K3qRMamp8KaWEZYcbNOGpSegwt_MCU3dKHOVLokZcafb13WyfbEyy90bQTcCNoI9rf_WmExZfs_foF5Q8NG5dg1reFHoQAWjxyMMzBBfjnBTbvbgj8DqDg-RiOhLZAqoMy3AQuCAdYbELuWl_PP3yeAxxuBEGKn4vDIuO2CwGtIjL9GD0Xbat_K0GsWNhRroN4vLN0RMFp186MRS2SwhM6DvC9btO_NPgb5efAh8pqb0zSdd8vw9tOG0D5b-Xr-YVVG2kEtvt_2TTz2mu1bp-BiDaKkh-OE4mA"


final_azure_count = 0
trans_final =0
success_final=0
in_progress_final=0
trans_failed=0


# access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjUzZWFiMDBhNzc5MTk3Yzc0MWQ2NjJmY2EzODE1OGJkN2JlNGEyY2MiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3VzbWl0IFN1cndhZGUiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXMtYWktYXV0aCIsImF1ZCI6ImVzLWFpLWF1dGgiLCJhdXRoX3RpbWUiOjE3MDY4ODI5NTYsInVzZXJfaWQiOiJXQUc4NVhpbXlSY0ZnOFRwa21Hbk9FSWtBTUIzIiwic3ViIjoiV0FHODVYaW15UmNGZzhUcGttR25PRUlrQU1CMyIsImlhdCI6MTcwNzExNTk5MiwiZXhwIjoxNzA3MTE5NTkyLCJlbWFpbCI6InN1c21pdC5zdXJ3YWRlQGJsZW5oZWltY2hhbGNvdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsibWljcm9zb2Z0LmNvbSI6WyI2ZTNiNTcxNy1kZTNlLTRmNGYtYjBlOC02ODc3MzBiNjE3YjUiXSwiZW1haWwiOlsic3VzbWl0LnN1cndhZGVAYmxlbmhlaW1jaGFsY290LmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Im1pY3Jvc29mdC5jb20ifX0.N-3d3dz02z9Uvsrl2sPK-gwsA8UL2Q6-iuVNsqSCQ_W3i1YuM7EzOHLNzxrNy64dr1N-EBpyUErRuxzMzX50_GrC96b-dH6AVD6khy56YjU5bIXae0sO-aQOoG3UTFu2EJAEGAIiA9dtDyqpXzzyfZsfNB8JxpYuZ_5NN26PPMgZPqAQCISRnLJ8sWqAhi4DEuHm0qtT37ds-tCvFODlPZr2MGYVPe2xEvP_PbVFiAXrHcGPTdfd2iAWnI6Pyoz7Ica-1Rb7DcuWtQgSHSBE4NawXdCKDJTU1rjqwARJ9feefTWGScF-2bgkCm-OzDbWuMCTW_EjHqQz-__EYCNs1w"

def count_files(account_name, account_key, container_name, modified_date):
    try:

        file_count = 0

        from azure.storage.blob import BlobServiceClient

        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        blobs = container_client.list_blobs()

        modified_date = datetime.fromisoformat(modified_date)

        for blob in blobs:
            last_modified = blob.last_modified
            if last_modified:
                if last_modified >= modified_date.replace(tzinfo=timezone.utc):
                    file_count += 1

        return file_count / 2
    except Exception as e:
        print(e)


#@pytest.mark.skip(reason="Reason for skipping the test function")
def test_Azure_file_counts():
        global afile_count
        account_name = "escommscoachinbound"
        account_key = "NlaxHb6fioxyYAWOUFhCli4QLRoiPDmTXPrKNuSij+mNQdC+N8WNQxsyRke5xaeM2TGT5R1PWBcz+AStDXnptw=="
        container_name = "oakbrook"
        today_date = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        date_str = f"{today_date}, 18:31:00"
        #date_str = "13/03/2024, 18:31:00"
        date_format = "%d/%m/%Y, %H:%M:%S"
        parsed_date = datetime.strptime(date_str, date_format)
        modified_date = parsed_date.isoformat()
        #modified_date_str = "28/02/2024, 11:47:30" # March 13, 2024, 12:00 AM in ISO 8601 format
        #modified_date = datetime.fromisoformat(modified_date_str)
        afile_count =int(count_files(account_name, account_key, container_name, modified_date))
        print(f"\n Number of files uploaded on Azure are : {afile_count}")

def test_refresh_token():
    global access_token
    url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyCz1XmsF38COosTR5crCZh8p8ZsAVCaNgM"

    payload = 'grant_type=refresh_token&refresh_token=AMf-vByaPgSKFOaJW1S4Zu0iv7E-PpLnrp7WfKwqdzUgWqhimzpH38cJ3TcoISgsUzxc21wi3XfPcWvinA_HUqBQbrUAtf1eHZhcWopNDj-AhgYXRo4KhZit8h6gHI4jx9QCWZTT-MN-E9HK3XgTjJYeebMbBrZvMHqCBYvB1PQ8oZt76SOl9CVPKZsAN5ADST_B5oeA-F3vWpr_lXGtLNnnL8MHZ-VyEMGf36J-8vt5HCpCJzzP1VjyNZNO8n-xUo3tb3MLaLaFscIXaPYr5-ZRc9mqfycxb4uz4jQ3HROCOdDHo8srgoTTVj_TfT6UsbWUIE9GJ6X7'
    headers = {
        'authority': 'securetoken.googleapis.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://comms-coach.englishscore.com',
        'referer': 'https://comms-coach.englishscore.com/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-client-data': 'CJG2yQEIorbJAQipncoBCLL8ygEIk6HLAQjnocsBCIWgzQEIuMjNAQii7s0BCIPwzQEY9cnNARin6s0BGMn4zQE=',
        'x-client-version': 'Chrome/JsCore/10.1.0/FirebaseCore-web',
        'x-firebase-gmpid': '1:928966609654:web:d3e7b34981ad35a0c37ad7'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    access_token = json_response["access_token"]
    return access_token

#@pytest.mark.skip(reason="Reason for skipping the test function")
def test_transcribed_count():
    access_token = test_refresh_token()
    url = f"https://cms.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:ASC&filters[$and][0][createdAt][$gt]={today_date}&filters[$and][1][status][$ne]=in-progress"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        #'Authorization': f'Bearer {access_token}',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImlhdCI6MTcxMDg2NjMwMywiZXhwIjoxNzEzNDU4MzAzfQ.dEKeQmWvgG3QGwCFuhXFppEdrfE7II9uSWU7mwXMIMQ',
        'Connection': 'keep-alive',
        'Origin': 'https://comms-coach.englishscore.com',
        'Referer': 'https://comms-coach.englishscore.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    trans_total = json_response["pagination"]["total"]
    print("\n Total Transcribbed  " + str(trans_total))
    global trans_final
    trans_final = trans_total

def test_success_count():
    access_token = test_refresh_token()
    url = f"https://cms.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:ASC&filters[$and][0][createdAt][$gt]={today_date}&filters[$and][1][status][$eq]=success"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        #'Authorization': f'Bearer {access_token}',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImlhdCI6MTcxMDg2NjMwMywiZXhwIjoxNzEzNDU4MzAzfQ.dEKeQmWvgG3QGwCFuhXFppEdrfE7II9uSWU7mwXMIMQ',
        'Connection': 'keep-alive',
        'Origin': 'https://comms-coach.englishscore.com',
        'Referer': 'https://comms-coach.englishscore.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    success_total = json_response["pagination"]["total"]
    print("\n Total success  " + str(success_total))
    global success_final
    success_final = success_total

def test_in_progress_count():
    access_token = test_refresh_token()
    url = f"https://cms.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:ASC&filters[$and][0][createdAt][$gt]={today_date}&filters[$and][1][status][$eq]=transcribed"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        #'Authorization': f'Bearer {access_token}',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImlhdCI6MTcxMDg2NjMwMywiZXhwIjoxNzEzNDU4MzAzfQ.dEKeQmWvgG3QGwCFuhXFppEdrfE7II9uSWU7mwXMIMQ',
        'Connection': 'keep-alive',
        'Origin': 'https://comms-coach.englishscore.com',
        'Referer': 'https://comms-coach.englishscore.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    in_progress_total = json_response["pagination"]["total"]
    print("\n Total In progress  " + str(in_progress_total))
    global in_progress_final
    in_progress_final = in_progress_total

def test_trancription_failed_count():
    access_token = test_refresh_token()
    url = f"https://cms.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:ASC&filters[$and][0][createdAt][$gt]={today_date}&filters[$and][1][status][$eq]=in-progress"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        #'Authorization': f'Bearer {access_token}',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMsImlhdCI6MTcxMDg2NjMwMywiZXhwIjoxNzEzNDU4MzAzfQ.dEKeQmWvgG3QGwCFuhXFppEdrfE7II9uSWU7mwXMIMQ',
        'Connection': 'keep-alive',
        'Origin': 'https://comms-coach.englishscore.com',
        'Referer': 'https://comms-coach.englishscore.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    trans_failed_total = json_response["pagination"]["total"]
    print("\n Total In progress  " + str(trans_failed_total))
    global trans_failed
    trans_failed = trans_failed_total


def test_send_mail():
    # AWS SMTP credentials
    smtp_username = 'AKIA5YBB6OJ66G2MXV7B'
    smtp_password = 'BMX8OsOi7Gy4OLgEsaKvyICJQbDOYv8XVEHtE2DGcLIE'
    smtp_hostname = 'email-smtp.eu-west-1.amazonaws.com'
    smtp_port = 587  # Adjust the port if necessary

    # Sender and recipient email addresses
    sender_email = 'no-reply@mail.englishscore.com'
    # Recipient email address
    recipient_emails = ["susmit.surwade@blenheimchalcot.com"]
    #recipient_emails = ["satyendra.kumar@blenheimchalcot.com","jeff.miranda@blenheimchalcot.com","susmit.surwade@blenheimchalcot.com", "lokesh.singh@blenheimchalcot.com", "ruksar.khan@blenheimchalcot.com","ami.jambusaria@blenheimchalcot.com","rinkesh.das@blenheimchalcot.com"]

    # Variables with total count and success count
    success_count = success_final
    transcribed_count = trans_final
    in_progress_count = in_progress_final
    azure_count = afile_count
    transcription_failed_count=trans_failed



    # Create message container
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Brocaly Support', sender_email))
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = f"Daily Report: Files Count Monitoring (12AM - 11:59PM) - {today_date_mail} IST"

    # body = f" Files received in CMS today as below: \n Organisation: Oakbrook \n Total Count: {total_count}\n Success Count: {success_count}\n Failed Count: {failed_count}\n Transcribed Count: {transcribed_count} "
    body = f"""
    <html>
      <body>
        <p><b>Files count showing on CMS portal on {today_date_mail} IST as below:</b></p>
        <table border="1">
            <tr>
                <td>Organisation:</td>
                <td style="text-align: center; padding-left: 10px; padding-right: 10px;">Oakbrook</td>
            </tr>
              <tr>
                <td>File Type:</td>
                <td style="text-align: center; padding-left: 10px; padding-right: 10px;">Voice</td>
            </tr>
            <tr>
                <td>Total Files Received in Azure blob storage:</td>
                <td style="text-align: center;">{azure_count}</td>
            </tr>
            <tr>
                <td>Total Transcribed to database:</td>
                <td style="text-align: center;">{transcribed_count}</td>
            </tr>
            <tr>
                <td>Total Evaluations Reports Ready:</td>
                <td style="text-align: center;">{success_count}</td>
            </tr>
            <tr>
                <td>Total Evaluations In progress:</td>
                <td style="text-align: center;">{in_progress_count}</td>
            </tr>
             <tr>
                <td>Total Transcription Failed:</td>
                <td style="text-align: center;">{transcription_failed_count}</td>
            </tr>
        </table>
           

        <p>For support/complaints/suggestions, please feel free to reach out to: <b>Service.Desk@brocaly.com</b><br>We’ll be happy to assist.<br>Regards,<br>Team Brocaly.</p>
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

