import json
import smtplib
import pytest
import requests
import pytz
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from azure.storage.blob import BlobServiceClient

yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%d/%m/%Y") # Keep 1 Day before date ie day=1
today_date = (datetime.now(pytz.timezone('Asia/Kolkata')) - timedelta(days=0)).strftime("%d-%m-%Y %H:%M:%S") # Keep today's Day before date ie day=0
search_string = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d") # Keep 1 Day before date ie day=1
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5NjI5NzU5NmJiNWQ4N2NjOTc2Y2E2YmY0Mzc3NGE3YWE5OTMxMjkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3VzbWl0IFN1cndhZGUiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXMtYWktYXV0aCIsImF1ZCI6ImVzLWFpLWF1dGgiLCJhdXRoX3RpbWUiOjE3MDY4ODI5NTYsInVzZXJfaWQiOiJXQUc4NVhpbXlSY0ZnOFRwa21Hbk9FSWtBTUIzIiwic3ViIjoiV0FHODVYaW15UmNGZzhUcGttR25PRUlrQU1CMyIsImlhdCI6MTcwNzA3NDMyNCwiZXhwIjoxNzA3MDc3OTI0LCJlbWFpbCI6InN1c21pdC5zdXJ3YWRlQGJsZW5oZWltY2hhbGNvdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsibWljcm9zb2Z0LmNvbSI6WyI2ZTNiNTcxNy1kZTNlLTRmNGYtYjBlOC02ODc3MzBiNjE3YjUiXSwiZW1haWwiOlsic3VzbWl0LnN1cndhZGVAYmxlbmhlaW1jaGFsY290LmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Im1pY3Jvc29mdC5jb20ifX0.k32njBhaAYv0zM6vSXIcxEVqXsQSja4bbd4PM2I5bChb1kvJjCa9K3qRMamp8KaWEZYcbNOGpSegwt_MCU3dKHOVLokZcafb13WyfbEyy90bQTcCNoI9rf_WmExZfs_foF5Q8NG5dg1reFHoQAWjxyMMzBBfjnBTbvbgj8DqDg-RiOhLZAqoMy3AQuCAdYbELuWl_PP3yeAxxuBEGKn4vDIuO2CwGtIjL9GD0Xbat_K0GsWNhRroN4vLN0RMFp186MRS2SwhM6DvC9btO_NPgb5efAh8pqb0zSdd8vw9tOG0D5b-Xr-YVVG2kEtvt_2TTz2mu1bp-BiDaKkh-OE4mA"
gurl = f"https://cms.comms-coach.englishscore.com/api/org/2/imported-conversations?filters[startDate]={yesterday}&filters[endDate]={yesterday}&filters[conversationType][0]=Voice&page=1&sort=-startDate"

final_success_count = 0
final_transcribed_count = 0
final_azure_count = 0


# access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjUzZWFiMDBhNzc5MTk3Yzc0MWQ2NjJmY2EzODE1OGJkN2JlNGEyY2MiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3VzbWl0IFN1cndhZGUiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXMtYWktYXV0aCIsImF1ZCI6ImVzLWFpLWF1dGgiLCJhdXRoX3RpbWUiOjE3MDY4ODI5NTYsInVzZXJfaWQiOiJXQUc4NVhpbXlSY0ZnOFRwa21Hbk9FSWtBTUIzIiwic3ViIjoiV0FHODVYaW15UmNGZzhUcGttR25PRUlrQU1CMyIsImlhdCI6MTcwNzExNTk5MiwiZXhwIjoxNzA3MTE5NTkyLCJlbWFpbCI6InN1c21pdC5zdXJ3YWRlQGJsZW5oZWltY2hhbGNvdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsibWljcm9zb2Z0LmNvbSI6WyI2ZTNiNTcxNy1kZTNlLTRmNGYtYjBlOC02ODc3MzBiNjE3YjUiXSwiZW1haWwiOlsic3VzbWl0LnN1cndhZGVAYmxlbmhlaW1jaGFsY290LmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Im1pY3Jvc29mdC5jb20ifX0.N-3d3dz02z9Uvsrl2sPK-gwsA8UL2Q6-iuVNsqSCQ_W3i1YuM7EzOHLNzxrNy64dr1N-EBpyUErRuxzMzX50_GrC96b-dH6AVD6khy56YjU5bIXae0sO-aQOoG3UTFu2EJAEGAIiA9dtDyqpXzzyfZsfNB8JxpYuZ_5NN26PPMgZPqAQCISRnLJ8sWqAhi4DEuHm0qtT37ds-tCvFODlPZr2MGYVPe2xEvP_PbVFiAXrHcGPTdfd2iAWnI6Pyoz7Ica-1Rb7DcuWtQgSHSBE4NawXdCKDJTU1rjqwARJ9feefTWGScF-2bgkCm-OzDbWuMCTW_EjHqQz-__EYCNs1w"


def count_files_with_string(account_name, account_key, container_name, search_string):
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Initialize count variable
    file_count = 0

    # List blobs in the container
    blobs = container_client.list_blobs()

    # Iterate over blobs and count those containing the search string
    for blob in blobs:
        name = blob.name
        if search_string in blob.name and name.endswith('.wav'):
            file_count += 1
    return file_count

    # target_date = datetime.now().replace(tzinfo=None)-timedelta(days=1)
    # for blob in blobs:
    # if blob.creation_time and blob.creation_time.replace(tzinfo=None) > target_date:
    # file_count += 1
    # return file_count


# if __name__ == "__main__":
#@pytest.mark.skip()
def test_azure_blob_count():
    global afile_count
    # Replace these with your Azure Storage account details

    # account_name = "susmit"
    # account_key = "B5gjKGSC0QK8TvPkWvKFSx6+8RbJ6sPwgDQgztIEIodwiekA6yO/eVy+htOBbKGEBsV3SX381Jrh+AStoAR/eA=="
    # container_name = "susmitcont"

    account_name = "escommscoachinbound"
    account_key = "NlaxHb6fioxyYAWOUFhCli4QLRoiPDmTXPrKNuSij+mNQdC+N8WNQxsyRke5xaeM2TGT5R1PWBcz+AStDXnptw=="
    container_name = "oakbrook"
    # Specify the search string "yyyymmdd"


    # Get the count of files containing the search string
    afile_count = count_files_with_string(account_name, account_key, container_name, search_string)
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


def test_listing_total_count():
    global TCount
    access_token = test_refresh_token()
    global page_no
    url = gurl
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {access_token}',
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
    TCount = json_response["meta"]["total"]
    print("\n Today's Total Count of file is " + str(TCount))
    page_no = json_response["meta"]["pageCount"]
    return page_no


@pytest.mark.parametrize("page_number", range(1, test_listing_total_count() + 1))
# @pytest.mark.parametrize("page_number", range(1, 3))
def test_listing_sucess_fail_records(page_number):
    success_count = 0
    transcribed_count = 0
    url = f"https://cms.comms-coach.englishscore.com/api/org/2/imported-conversations?filters[startDate]={yesterday}&filters[endDate]={yesterday}&filters[conversationType][0]=Voice&page={page_number}&sort=-startDate"
    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {access_token}',
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

    # SCount = json_response["pagination"]["total"]
    # print("\n Today's Success Count is " + str(SCount))
    # json_format=json.dumps(json_response, indent=2)
    # print(json_format)
    for item in json_response["data"]:
        conversation_status = item.get("conversation_status")
        if conversation_status == "success":
            success_count += 1
        if conversation_status == "transcribed":
            transcribed_count += 1

    global final_success_count
    final_success_count += success_count
    global final_transcribed_count
    final_transcribed_count += transcribed_count
    print(f"\n Running test for page {page_number}")
    # print(final_success_count)
    # print(final_transcribed_count)

"""
def test_print_counts():
    print(f"\n Number of successful conversations ie Status = Report Ready: {final_success_count}")
    print(f"\n Number of transcribed conversations ie Status = In progress: {final_transcribed_count}")
"""

def test_send_mail():
    # Your email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "susmit.s.surwade@gmail.com"
    smtp_password = "qzod ltfm nmav tqvw"

    # Recipient email address
    #recipient_emails = ["susmit.surwade@blenheimchalcot.com"]
    recipient_emails = ["rinkesh.das@englishscore.com","ami.jambusaria@englishscore.com","susmit.surwade@blenheimchalcot.com", "lokesh.singh@blenheimchalcot.com", "ruksar.khan@blenheimchalcot.com","ami.jambusaria@blenheimchalcot.com","rinkesh.das@blenheimchalcot.com"]

    # Variables with total count and success count
    total_count = TCount
    success_count = final_success_count
    transcribed_count = final_transcribed_count
    azure_count = afile_count

    # Format today's date
    #today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #today_date = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%Y %H:%M:%S")

    # Create the email message
    subject = f"Daily Report: Voice Files Count Monitoring (12AM - 11:59PM) - {today_date}(IST)"
    # body = f" Files received in CMS today as below: \n Organisation: Oakbrook \n Total Count: {total_count}\n Success Count: {success_count}\n Failed Count: {failed_count}\n Transcribed Count: {transcribed_count} "
    body = f"""
    <html>
      <body>
        <p><b>Voice Files count showing on PRODUCTION Brocaly portal on {today_date}(IST) as below:</b></p>
        <table border="1">
            <tr>
                <td>Organisation:</td>
                <td style="text-align: center;">Oakbrook</td>
            </tr>
            <tr>
                <td>Total Files Received in Azure blob storage:</td>
                <td style="text-align: center;">{azure_count}</td>
            </tr>
            <tr>
                <td>Total Files Received in CMS:</td>
                <td style="text-align: center;">{total_count}</td>
            </tr>
            <tr>
                <td>Total Evaluations Reports Ready:</td>
                <td style="text-align: center;">{success_count}</td>
            </tr>
            <tr>
                <td>Total Evaluations In progress:</td>
                <td style="text-align: center;">{transcribed_count}</td>
            </tr>
        </table>
      </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = smtp_username
    # message["To"] = recipient_email
    message['To'] = ', '.join(recipient_emails)
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        # server.sendmail(smtp_username, recipient_email, message.as_string())
        for recipient_email in recipient_emails:
            server.sendmail(smtp_username, recipient_email, message.as_string())
    print("\n Email sent successfully.")
