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

yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%d/%m/%Y")  # Keep 1 Day before date ie day=1
today_date = (datetime.now(pytz.timezone('Asia/Kolkata')) - timedelta(days=0)).strftime("%d-%m-%Y %H:%M:%S")  # Keep today's Day before date ie day=0
# search_string = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")  # Keep 1 Day before date ie day=1
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5NjI5NzU5NmJiNWQ4N2NjOTc2Y2E2YmY0Mzc3NGE3YWE5OTMxMjkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3VzbWl0IFN1cndhZGUiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXMtYWktYXV0aCIsImF1ZCI6ImVzLWFpLWF1dGgiLCJhdXRoX3RpbWUiOjE3MDY4ODI5NTYsInVzZXJfaWQiOiJXQUc4NVhpbXlSY0ZnOFRwa21Hbk9FSWtBTUIzIiwic3ViIjoiV0FHODVYaW15UmNGZzhUcGttR25PRUlrQU1CMyIsImlhdCI6MTcwNzA3NDMyNCwiZXhwIjoxNzA3MDc3OTI0LCJlbWFpbCI6InN1c21pdC5zdXJ3YWRlQGJsZW5oZWltY2hhbGNvdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsibWljcm9zb2Z0LmNvbSI6WyI2ZTNiNTcxNy1kZTNlLTRmNGYtYjBlOC02ODc3MzBiNjE3YjUiXSwiZW1haWwiOlsic3VzbWl0LnN1cndhZGVAYmxlbmhlaW1jaGFsY290LmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Im1pY3Jvc29mdC5jb20ifX0.k32njBhaAYv0zM6vSXIcxEVqXsQSja4bbd4PM2I5bChb1kvJjCa9K3qRMamp8KaWEZYcbNOGpSegwt_MCU3dKHOVLokZcafb13WyfbEyy90bQTcCNoI9rf_WmExZfs_foF5Q8NG5dg1reFHoQAWjxyMMzBBfjnBTbvbgj8DqDg-RiOhLZAqoMy3AQuCAdYbELuWl_PP3yeAxxuBEGKn4vDIuO2CwGtIjL9GD0Xbat_K0GsWNhRroN4vLN0RMFp186MRS2SwhM6DvC9btO_NPgb5efAh8pqb0zSdd8vw9tOG0D5b-Xr-YVVG2kEtvt_2TTz2mu1bp-BiDaKkh-OE4mA"
# gurl = f"https://cms.comms-coach.englishscore.com/api/org/2/imported-conversations?filters[startDate]={yesterday}&filters[endDate]={yesterday}&filters[conversationType][0]=Voice&page=1&sort=-startDate"
gurl = f"https://prd-brocaly-d0d5h0a3deaedvbq.z02.azurefd.net/api/org/2/imported-conversations?filters[startDate]={yesterday}&filters[endDate]={yesterday}&filters[conversationType][0]=Voice&page=1&sort=-startDate"
final_success_count = 0
final_transcribed_count = 0
final_azure_count = 0
final_transcribed_sucess = 0


# access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjUzZWFiMDBhNzc5MTk3Yzc0MWQ2NjJmY2EzODE1OGJkN2JlNGEyY2MiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU3VzbWl0IFN1cndhZGUiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXMtYWktYXV0aCIsImF1ZCI6ImVzLWFpLWF1dGgiLCJhdXRoX3RpbWUiOjE3MDY4ODI5NTYsInVzZXJfaWQiOiJXQUc4NVhpbXlSY0ZnOFRwa21Hbk9FSWtBTUIzIiwic3ViIjoiV0FHODVYaW15UmNGZzhUcGttR25PRUlrQU1CMyIsImlhdCI6MTcwNzExNTk5MiwiZXhwIjoxNzA3MTE5NTkyLCJlbWFpbCI6InN1c21pdC5zdXJ3YWRlQGJsZW5oZWltY2hhbGNvdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsibWljcm9zb2Z0LmNvbSI6WyI2ZTNiNTcxNy1kZTNlLTRmNGYtYjBlOC02ODc3MzBiNjE3YjUiXSwiZW1haWwiOlsic3VzbWl0LnN1cndhZGVAYmxlbmhlaW1jaGFsY290LmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Im1pY3Jvc29mdC5jb20ifX0.N-3d3dz02z9Uvsrl2sPK-gwsA8UL2Q6-iuVNsqSCQ_W3i1YuM7EzOHLNzxrNy64dr1N-EBpyUErRuxzMzX50_GrC96b-dH6AVD6khy56YjU5bIXae0sO-aQOoG3UTFu2EJAEGAIiA9dtDyqpXzzyfZsfNB8JxpYuZ_5NN26PPMgZPqAQCISRnLJ8sWqAhi4DEuHm0qtT37ds-tCvFODlPZr2MGYVPe2xEvP_PbVFiAXrHcGPTdfd2iAWnI6Pyoz7Ica-1Rb7DcuWtQgSHSBE4NawXdCKDJTU1rjqwARJ9feefTWGScF-2bgkCm-OzDbWuMCTW_EjHqQz-__EYCNs1w"


#@pytest.mark.skip(reason="Reason for skipping the test function")
def test_Azure_file_counts():
    global afile_count
    # Your connection string
    # connection_string = "DefaultEndpointsProtocol=https;AccountName=bldevuksouthevtsta;AccountKey=zGvS2VUse2PWOHz6EhIxAb0BT5j+kpS2l2gdH0BqvOr7aq+aNk35C8euInI5oOZjdv83qeytD6cT+ASt7gKBDQ==;EndpointSuffix=core.windows.net"
    connection_string = "DefaultEndpointsProtocol=https;AccountName=blprduksouthevtsta;AccountKey=scciDAiG/KakT0wwK0RX281SFE9tTei3vK0XOz21f4Dm0nyD4+PjOGtBtwEIE+0+yR47Id+UgAyV+ASt6IQ+aA==;EndpointSuffix=core.windows.net"
    container_name = "liberis"
    blob_path = "to-be-processed/"

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)

    # Define the cutoff time
    now = datetime.now(timezone.utc)
    yesterdayaz = now - timedelta(days=1)
    cutoff_time = yesterdayaz.replace(hour=18, minute=0, second=0, microsecond=0)
    cutoff_time_str = cutoff_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    # cutoff_time_str = '2024-04-12T06:32:42.000Z'
    # cutoff_time = datetime.strptime(cutoff_time_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)

    # Fetch the list of blobs and count those created after the cutoff time
    blob_list = container_client.list_blobs(name_starts_with=blob_path)
    count = 0

    for blob in blob_list:
        blob_properties = container_client.get_blob_client(blob).get_blob_properties()
        creation_time = blob_properties['last_modified']
        if creation_time > cutoff_time:
            count += 1

    print(f"Number of files uploaded after {cutoff_time_str}: {count}")
    afile_count = count

"""
@pytest.mark.skip(reason="Reason for skipping the test function")
def test_refresh_token():
    global access_token
    url = "https://login.microsoftonline.com/a08d8e40-4cc5-47a0-81d3-c43ba1ffcb5c/oauth2/v2.0/token"

    payload = "client_id=16f9d357-3ffe-40dc-9039-29f9b14d810e&scope=api%3A%2F%2F5c1bd365-0696-410b-ac58-a11b8ca3c72b%2F.default%20openid%20profile%20offline_access&grant_type=refresh_token&client_info=1&x-client-SKU=msal.js.browser&x-client-VER=3.10.0&x-ms-lib-capability=retry-after, h429&x-client-current-telemetry=5|61,0,,,|,&x-client-last-telemetry=5|0|||0,0&client-request-id=018f7cc7-3d1d-7811-8869-f6cbcd92aced&refresh_token=0.Aa4AQI6NoMVMoEeB08Q7of_LXFfT-Rb-P9xAkDkp-bFNgQ6rADE.AgABAwEAAADnfolhJpSnRYB1SVj-Hgd8AgDs_wUA9P-m-xViL6d-e8J7uzxXytXEJZedCztp1yX7TTHWKqJ97uDf5zEeeIGk-YFn7xIpul6TTkbebrAlcIItr3sXstQsvNdRfK1Z1VhuAQCb9-a52PluhaROT_eOGEarEWJFzd2V4fF7v935iRQExPvAcgfJC12XZQIIw-RIwdDuaRVIYqQcL9R-R3QhfiUVsmPViFKsRhis1XQ1phCdXaPiZ0KIpr4PcpbTTEfeoeK6MtSCOHF6kTQlCU7T_J5YnjEEqCzPEyDZv4_TsfVzJYxew2VAFvMYHOQCtcf4U49MfSJskO0eGPHRsWswkSIhy-vOS58r3Ap7zlNrDJ5FrSDGmKz1T1koz-LcOwsLxHEAXIOAf5s_hPdjVnr0pvLpVsVI2wCChSLMQrONdYqPi1HmtMax2iGmu2kuU8PJ2MbmfadXdgBxx5Q9IKPRiNmDqXbU5LzQAu21Z2BKpY41sPJaMejdhnZBv3OShsEhj_k1FYDCPsrYVtKuhKXjk61eoS7VRSqBHOjqXkSJjs-ffMj_guD6ORYCZqtGzkvM-cl47hgspwCISFBdowla7DN-3pzYDVJIdIaohrCwQsgysBDI2QBDEDffpIgP-HonxGMcHLrWb7CKeFRMc0RbtpRx9QL3U38KmSQJWgQ2Lpen8Z518TJOF9ribq1UICaSejgFi7l3tDOo7bsBp21tF3LogD6Lb521br7AJkCxfHnbCjO3s8m2VqkU71_nsIUw_YJPZ3VEmp6cDzNNnsg2oGquY3Sxb2v-sB-OGCOxHWWULMbectTKX0_5CdMaK_uov3hwR-9uxsI3KVITHWd1BnPKh1jIlfewKbrLFpBWYQHV5B-rcMKNGytnjjUTvWVFXKOH92j49_TUk2tmVvW1iUef7EfjhIvRYXLUQqIgvEM5Ja1vAULdcfGlmRRTX00JdXKtUuK5Gs0BUz-X8uoPyN3KE0N_F9TjqwawCo2wQdba7fHFd03tqN65M2dQ8GpIf8iIzosMqcTGzBU7Kh85iXXbvExlmlPSs0BnYUICbx1GClmBPHzrcSnTJMO8d6bVc6BQg4aYxt3vB_68qheGrARTXa-Bo-uZy-NwH8kTiT-7DN6Gj2-_dqot05eZTqwJdzapQq20GGaF5Hut18bIo8vki5PlOUPei3hx4QG-4wdHGOdnZ_s&X-AnchorMailbox=Oid%3A6e3b5717-de3e-4f4f-b0e8-687730b617b5%40dd5343bd-f2c4-4f9b-8178-8dfb6445911b"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'origin': 'https://prd-brocaly-d0d5h0a3deaedvbq.z02.azurefd.net',
        'priority': 'u=1, i',
        'referer': 'https://prd-brocaly-d0d5h0a3deaedvbq.z02.azurefd.net/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Cookie': 'fpc=AiS_UZrYAVlHm3pTW4pc0xUxvaQxAQAAABqm190OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    access_token = json_response["access_token"]
    return access_token
"""

def test_refresh_token():
    global access_token
    refresh_token="0.Aa4AQI6NoMVMoEeB08Q7of_LXFfT-Rb-P9xAkDkp-bFNgQ6rAD4.AgABAwEAAADnfolhJpSnRYB1SVj-Hgd8AgDs_wUA9P-lu52ZYBULrgvJvN-bN5CIer6ohcDZckcTMXUQzi_eRf4Y7clI9HpXgYBhqtv6iBRNDtvaNdWfB9wHhnXZrFR5xun_FkJKZeRY12Pbr4sCjKd3MmK2HItUiG5XgqwJouRm4GTCHkSgxwnUjlmaNlafPJ4wgKvFRjAlTMjEOrN620OAdL9QH3kuPueTB8bmheKd8B-RHl9g1IJMLYte8rxi56Jr3dSOY_StxhDjHT8W8KQcgeeiUUEzHzI31f8JjsC3jkboFD04M4dA3x-9ufH3Uee6j6f8grnQFxCgP_z_XlgC6pcZw_7k2BjPKTpmfqf_k4ENhRadrw6nvcpAYnsTtFu8TLVVQdk3ixSj-5jPqKRllLmV9e49wqruLoOB0SOMkAf3n6z_IQbhJLuG4rsLu7SedAC2gD6GbfO34C-L_Yjb3KwdsCQeBXLfHBasHSCmiC7kHjyD-w5PazLnJcxpe7mMkt9O0zyP4R9TPAZJXvVmEQ324QklBgg5xM3MKijSvpYak8o4wC00JY0buHxnlqUTyP-SxM6qdJNLybHECZXQFhxfC2TINpHxEVqOcwlt5M3r2eZl6Gyqn077uQQzJWZATg_DoERO4olfjv8dCtvO0pYj_wE3GdQFf_DE3yML0pVCMHj-DhIcQf9kOx6rpAUeX8Zs3Kxs7ykfIDM4y-bw5yuacty-JMZADOAllfHSOMfBRXlLVixMelm3MC7Y9ov8iOI3GFNJZeAd1s6PQR0ONftsQGLp0z_r2P5SjWosY5vY-kSYhsHyH7A0jni2YeV6btyhweI9zytrONXPRwQL8JUutR8tdj8thJ8wsqwDH1Nk-8dj0Ceextuz2Uhd7LKzM1EFHG6EnjEq6w0K4Q"
    url = "https://login.microsoftonline.com/a08d8e40-4cc5-47a0-81d3-c43ba1ffcb5c/oauth2/v2.0/token"
    payload = f"""
    client_id=16f9d357-3ffe-40dc-9039-29f9b14d810e&scope=api%3A%2F%2F5c1bd365-0696-410b-ac58-a11b8ca3c72b%2F.default%20openid%20profile%20offline_access&grant_type=refresh_token&client_info=1&x-client-SKU=msal.js.browser&x-client-VER=3.10.0&x-ms-lib-capability=retry-after, h429&x-client-current-telemetry=5|61,0,,,|,&x-client-last-telemetry=5|0|||0,0&client-request-id=018fc45e-3ddb-70dd-b714-e2a7962db9a9&refresh_token={refresh_token}&X-AnchorMailbox=Oid%3Abff03e80-44f4-4038-b3b2-b44711acb7cc%40a08d8e40-4cc5-47a0-81d3-c43ba1ffcb5c
    """
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
        'origin': 'https://prd-brocaly-d0d5h0a3deaedvbq.z02.azurefd.net',
        'priority': 'u=1, i',
        'referer': 'https://prd-brocaly-d0d5h0a3deaedvbq.z02.azurefd.net/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Cookie': 'buid=0.Aa4AQI6NoMVMoEeB08Q7of_LXFfT-Rb-P9xAkDkp-bFNgQ6rAAA.AQABGgEAAADnfolhJpSnRYB1SVj-Hgd8sA68yoNDUzpNnm2yctkG7iHuanKy5Pme2pKakH3ra8ra20-1SNzmcgziKurrH3oWWvoaqu36BuoRlTKmSA_I8hzdTDEQvIx0Ac5Pf-zDjhMgAA; fpc=AiS_UZrYAVlHm3pTW4pc0xUxvaQxAQAAAIEa6d0OAAAAd37W5QEAAADFHendDgAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    access_token = json_response["access_token"]
    print(access_token)
    return access_token



def test_listing_total_count():
    global TCount
    access_token = test_refresh_token()
    #access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCIsImtpZCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCJ9.eyJhdWQiOiJhcGk6Ly81YzFiZDM2NS0wNjk2LTQxMGItYWM1OC1hMTFiOGNhM2M3MmIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMDhkOGU0MC00Y2M1LTQ3YTAtODFkMy1jNDNiYTFmZmNiNWMvIiwiaWF0IjoxNzE2OTg2MTYyLCJuYmYiOjE3MTY5ODYxNjIsImV4cCI6MTcxNjk5MDcyNSwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhXQUFBQVlFZDc0NG1qU1c1Vkt6SW15Q2M1WXpkanJwcUZFMGxCV05GR3pPVnRBTGpYSVYzdE1OSkFqcnhqS2hwM0g0enRRQ0c1V2pVNHpiSUg4bHBvaVVWNDd2UnVBNS83d1pvOXNJWjVzelE4NGtBPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwaWQiOiIxNmY5ZDM1Ny0zZmZlLTQwZGMtOTAzOS0yOWY5YjE0ZDgxMGUiLCJhcHBpZGFjciI6IjAiLCJncm91cHMiOlsiZGQwZWY1MjItMjMyZi00N2FlLWEwOGUtOWYyODc5MDg2YmY2IiwiNDA1ZDcxNDgtMDYzMS00ZGFjLWJmYjYtYzIzZmJmZjEzNTgyIiwiNDU1ZTRmNDktN2Q0Zi00ODM1LWJmNjAtYTM4YTA5MWM0MDliIiwiNDEzODhjYjAtZTVmMS00NGEyLWE0MjgtYmYxNTYzOWE5MjQzIiwiNDdhZDA5YzgtMDIyOC00NzZhLWE0N2EtZDBjOTM2NjQzOWY2IiwiYjRlNWI5ZGUtNTNiMi00ODE0LWFkOWItNGQ0MmRkMmNmMmVmIiwiZmVhY2NmZWMtOWNkNS00ODU2LWI0M2QtODFjYTQ5MThkZjhlIiwiNDZiZDNkZjMtZWY2ZS00MzRmLWIwNjEtYmMzYTA0NmVmYzA0Il0sImlwYWRkciI6IjE4Mi40OC4yNTUuMjM4IiwibmFtZSI6IlN1c21pdCBMaWJlcmlzIiwib2lkIjoiYmZmMDNlODAtNDRmNC00MDM4LWIzYjItYjQ0NzExYWNiN2NjIiwicmgiOiIwLkFhNEFRSTZOb01WTW9FZUIwOFE3b2ZfTFhHWFRHMXlXQmd0QnJGaWhHNHlqeHl1ckFENC4iLCJzY3AiOiJiYWNrZW5kX2FwaSIsInN1YiI6ImpYMlNNV2VoRjlqelFEQnotaVpPNXFpQ3dGb2xJYmZEWlhJSVplZHNoZVkiLCJ0aWQiOiJhMDhkOGU0MC00Y2M1LTQ3YTAtODFkMy1jNDNiYTFmZmNiNWMiLCJ1bmlxdWVfbmFtZSI6InN1c21pdC5zdXJ3YWRlX29ha2Jyb29rQGJyb2NhbHkuY29tIiwidXBuIjoic3VzbWl0LnN1cndhZGVfb2FrYnJvb2tAYnJvY2FseS5jb20iLCJ1dGkiOiJJV3lISm9nYkdFYWI4SDlFbGlYdkFBIiwidmVyIjoiMS4wIn0.Ov1r7pM8J8xm5qlIuZP2jPkhe5KV3nHHFoxBfAdgpzUt4ategp9TPY_uZ8DfkfmdRaDHjuSLXDRLm1Kld-yV9Sq4mQVtxPCM35L8sIUE9i1e_JN6Sex775TP8pPzIqhvXiq2jmGs3KIHTeot_-G0bdUp53f2LiRUNxQWAVOaS2wUHgjaU0OXmMxhkLTwCgCNPXBMIBzlUmRVh1PyUGy8v1UKloHCD8AcOJgrRRSyHZrBbfiG1aFgVY16r2neoZqI2mM0s7Ev8ziFK-muHcv5bj2p4dO4WnDru5tMlQlISgXzKWLJvzdxqUZpMxn-xr90rKSqtsIrnHXaenhlOHP6Hg"
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
# @pytest.mark.parametrize("page_number", range(1, 2))
def test_listing_sucess_fail_records(page_number):
    success_count = 0
    transcribed_count = 0
    access_token = test_refresh_token()
    #access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCIsImtpZCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCJ9.eyJhdWQiOiJhcGk6Ly81YzFiZDM2NS0wNjk2LTQxMGItYWM1OC1hMTFiOGNhM2M3MmIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMDhkOGU0MC00Y2M1LTQ3YTAtODFkMy1jNDNiYTFmZmNiNWMvIiwiaWF0IjoxNzE2OTg2MTYyLCJuYmYiOjE3MTY5ODYxNjIsImV4cCI6MTcxNjk5MDcyNSwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhXQUFBQVlFZDc0NG1qU1c1Vkt6SW15Q2M1WXpkanJwcUZFMGxCV05GR3pPVnRBTGpYSVYzdE1OSkFqcnhqS2hwM0g0enRRQ0c1V2pVNHpiSUg4bHBvaVVWNDd2UnVBNS83d1pvOXNJWjVzelE4NGtBPSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwaWQiOiIxNmY5ZDM1Ny0zZmZlLTQwZGMtOTAzOS0yOWY5YjE0ZDgxMGUiLCJhcHBpZGFjciI6IjAiLCJncm91cHMiOlsiZGQwZWY1MjItMjMyZi00N2FlLWEwOGUtOWYyODc5MDg2YmY2IiwiNDA1ZDcxNDgtMDYzMS00ZGFjLWJmYjYtYzIzZmJmZjEzNTgyIiwiNDU1ZTRmNDktN2Q0Zi00ODM1LWJmNjAtYTM4YTA5MWM0MDliIiwiNDEzODhjYjAtZTVmMS00NGEyLWE0MjgtYmYxNTYzOWE5MjQzIiwiNDdhZDA5YzgtMDIyOC00NzZhLWE0N2EtZDBjOTM2NjQzOWY2IiwiYjRlNWI5ZGUtNTNiMi00ODE0LWFkOWItNGQ0MmRkMmNmMmVmIiwiZmVhY2NmZWMtOWNkNS00ODU2LWI0M2QtODFjYTQ5MThkZjhlIiwiNDZiZDNkZjMtZWY2ZS00MzRmLWIwNjEtYmMzYTA0NmVmYzA0Il0sImlwYWRkciI6IjE4Mi40OC4yNTUuMjM4IiwibmFtZSI6IlN1c21pdCBMaWJlcmlzIiwib2lkIjoiYmZmMDNlODAtNDRmNC00MDM4LWIzYjItYjQ0NzExYWNiN2NjIiwicmgiOiIwLkFhNEFRSTZOb01WTW9FZUIwOFE3b2ZfTFhHWFRHMXlXQmd0QnJGaWhHNHlqeHl1ckFENC4iLCJzY3AiOiJiYWNrZW5kX2FwaSIsInN1YiI6ImpYMlNNV2VoRjlqelFEQnotaVpPNXFpQ3dGb2xJYmZEWlhJSVplZHNoZVkiLCJ0aWQiOiJhMDhkOGU0MC00Y2M1LTQ3YTAtODFkMy1jNDNiYTFmZmNiNWMiLCJ1bmlxdWVfbmFtZSI6InN1c21pdC5zdXJ3YWRlX29ha2Jyb29rQGJyb2NhbHkuY29tIiwidXBuIjoic3VzbWl0LnN1cndhZGVfb2FrYnJvb2tAYnJvY2FseS5jb20iLCJ1dGkiOiJJV3lISm9nYkdFYWI4SDlFbGlYdkFBIiwidmVyIjoiMS4wIn0.Ov1r7pM8J8xm5qlIuZP2jPkhe5KV3nHHFoxBfAdgpzUt4ategp9TPY_uZ8DfkfmdRaDHjuSLXDRLm1Kld-yV9Sq4mQVtxPCM35L8sIUE9i1e_JN6Sex775TP8pPzIqhvXiq2jmGs3KIHTeot_-G0bdUp53f2LiRUNxQWAVOaS2wUHgjaU0OXmMxhkLTwCgCNPXBMIBzlUmRVh1PyUGy8v1UKloHCD8AcOJgrRRSyHZrBbfiG1aFgVY16r2neoZqI2mM0s7Ev8ziFK-muHcv5bj2p4dO4WnDru5tMlQlISgXzKWLJvzdxqUZpMxn-xr90rKSqtsIrnHXaenhlOHP6Hg"
    url = f"https://prd-brocaly-d0d5h0a3deaedvbq.z02.azurefd.net/api/org/2/imported-conversations?filters[startDate]={yesterday}&filters[endDate]={yesterday}&filters[conversationType][0]=Voice&page={page_number}&sort=-startDate"
    # url = f"https://cms.comms-coach.englishscore.com/api/org/2/imported-conversations?filters[startDate]={yesterday}&filters[endDate]={yesterday}&page={page_number}&sort=-startDate"
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
    global final_transcribed_sucess
    final_transcribed_sucess = final_success_count + final_transcribed_count
    print(f"\n Running test for page {page_number}")
    # print(final_success_count)
    # print(final_transcribed_count)


"""
def test_print_counts():
    print(f"\n Number of successful conversations ie Status = Report Ready: {final_success_count}")
    print(f"\n Number of transcribed conversations ie Status = In progress: {final_transcribed_count}")
"""


def test_send_mail():
    # AWS SMTP credentials
    smtp_username = 'AKIA5YBB6OJ66G2MXV7B'
    smtp_password = 'BMX8OsOi7Gy4OLgEsaKvyICJQbDOYv8XVEHtE2DGcLIE'
    smtp_hostname = 'email-smtp.eu-west-1.amazonaws.com'
    smtp_port = 587  # Adjust the port if necessary

    # Sender and recipient email addresses
    sender_email = 'no-reply@mail.englishscore.com'
    # Recipient email address
    recipient_emails = ["susmit.surwade@blenheimchalcot.com","satyendra.kumar@blenheimchalcot.com","ruksar.khan@blenheimchalcot.com"]
    #recipient_emails = ["satyendra.kumar@blenheimchalcot.com","jeff.miranda@blenheimchalcot.com","susmit.surwade@blenheimchalcot.com", "lokesh.singh@blenheimchalcot.com","ami.jambusaria@blenheimchalcot.com","rinkesh.das@blenheimchalcot.com",
    # "help@maxcontact.com","automation@maxcontact.com","dialler.team@sigmaconnected.com","vincent.khomola@sigmaconnected.com","jenna.barnes@sigmaconnected.com","nathier.davids@sigmaconnected.com","aashish.paruvada@blenheimchalcot.com"]

    # Variables with total count and success count
    total_count = TCount
    success_count = final_success_count
    transcribed_count = final_transcribed_count
    trans_success = final_transcribed_sucess
    #azure_count = afile_count
    azure_count = 0

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Brocaly Support', sender_email))
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = f"Daily Report: Voice Files Count Monitoring (12AM - 11:59PM) - {today_date} IST"

    # body = f" Files received in CMS today as below: \n Organisation: Oakbrook \n Total Count: {total_count}\n Success Count: {success_count}\n Failed Count: {failed_count}\n Transcribed Count: {transcribed_count} "
    body = f"""
    <html>
      <body>
        <p><b>Voice Files count showing on PRODUCTION Oakbrook portal on {today_date} IST as below:</b></p>
        <table border="1">
            <tr>
                <td>Organisation:</td>
                <td style="text-align: center;">Oakbrook</td>
            </tr>
            <tr>
                <td>Total Files Received in Azure Storage:</td>
                <td style="text-align: center;">{azure_count}</td>
            </tr>
            <tr>
                <td>Total Files Transcribed to Database:</td>
                <td style="text-align: center;">{trans_success}</td>
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
