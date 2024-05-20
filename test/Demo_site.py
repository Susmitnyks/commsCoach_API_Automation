import json

import pytest
import requests

def test_refresh_token_poc():
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
    #access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCIsImtpZCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCJ9.eyJhdWQiOiJhcGk6Ly81YzFiZDM2NS0wNjk2LTQxMGItYWM1OC1hMTFiOGNhM2M3MmIiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9hMDhkOGU0MC00Y2M1LTQ3YTAtODFkMy1jNDNiYTFmZmNiNWMvIiwiaWF0IjoxNzE1Nzg1MDgzLCJuYmYiOjE3MTU3ODUwODMsImV4cCI6MTcxNTc5MDM3NSwiYWNyIjoiMSIsImFpbyI6IkFRUUIrLzRXQUFBQVBiNHhjZllocWZ3SkZMSitScy9Pek1zcWVCVlBNbG9iNERlRkQ4T1JZOTRwcjNjU1NYYUhmQzVGOWZhVXNvWXg4a0FsUk9IbFdTNUtHdFgzYkJVaFkrSHpyWlBzQ0NwRTFLc1ZsUHlKdEhydjNYV0pzdUcyOUFVbndyUi9CbEMyR3lNbjVSbW5qNWl0bU9xSGFQZ0U5dU11UUdoWnFmK2wvRmFkQ2hnSC9SQ3hYZWZOMHl0VmEyeWJLbUVNblphaHgwZ0REUGtxVjNVK3BqK0xqNVZwd1BjUk1Gdkp1Z2Rha3NWM2dJVklwWFBHSnp5NFdUcFk1ZDEyd2RzVHFiTm9Cem5XUmFGSEM3dXhIbS9pVEtyZXVPbmp4N3BQTXR3cEhXUDZ3MzIxQVZ2YzBsTXJmVXdhRmtQMnh6U0luY1VGTWtDS21WSjcyNmhXcE1YTnFzSVlFQT09IiwiYW1yIjpbImZpZG8iLCJtZmEiXSwiYXBwaWQiOiIxNmY5ZDM1Ny0zZmZlLTQwZGMtOTAzOS0yOWY5YjE0ZDgxMGUiLCJhcHBpZGFjciI6IjAiLCJlbWFpbCI6InN1c21pdC5zdXJ3YWRlQGJsZW5oZWltY2hhbGNvdC5jb20iLCJncm91cHMiOlsiZGQwZWY1MjItMjMyZi00N2FlLWEwOGUtOWYyODc5MDg2YmY2IiwiN2UzYTZkMzctMTNjNy00YTZiLTk2NmQtMjBlZjc3YjBmYzU0IiwiNDA1ZDcxNDgtMDYzMS00ZGFjLWJmYjYtYzIzZmJmZjEzNTgyIiwiNDU1ZTRmNDktN2Q0Zi00ODM1LWJmNjAtYTM4YTA5MWM0MDliIiwiYWVhNGUxNTItNzJiNC00N2FkLTgxZmYtOGIwYzEzNjJmMzk0IiwiOGU5ZjM4OTEtZGQ2Ni00MDI1LWI1NzktNjhjZWJlZDZhZDgxIiwiNDdhZDA5YzgtMDIyOC00NzZhLWE0N2EtZDBjOTM2NjQzOWY2IiwiYjRlNWI5ZGUtNTNiMi00ODE0LWFkOWItNGQ0MmRkMmNmMmVmIiwiMjBhM2JkZWItOTUyMy00YmViLTlhNDktMjQyY2E4MmU5NGNiIiwiNDZiZDNkZjMtZWY2ZS00MzRmLWIwNjEtYmMzYTA0NmVmYzA0Il0sImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2RkNTM0M2JkLWYyYzQtNGY5Yi04MTc4LThkZmI2NDQ1OTExYi8iLCJpcGFkZHIiOiIyMDMuMTkyLjIwMS4yMjciLCJuYW1lIjoiU3VzbWl0IFN1cndhZGUiLCJvaWQiOiJlMGMwMDU2Yi03ZTFjLTQ1NjUtYjg0OS1hYzM0YWNlOGY1ODciLCJyaCI6IjAuQWE0QVFJNk5vTVZNb0VlQjA4UTdvZl9MWEdYVEcxeVdCZ3RCckZpaEc0eWp4eXVyQURFLiIsInNjcCI6ImJhY2tlbmRfYXBpIiwic3ViIjoiWjNUMzIzWXdMbHNPVjVLa0duVlNLQnRHSHlMMzNlVE5EWUUwNUxaaUwtNCIsInRpZCI6ImEwOGQ4ZTQwLTRjYzUtNDdhMC04MWQzLWM0M2JhMWZmY2I1YyIsInVuaXF1ZV9uYW1lIjoic3VzbWl0LnN1cndhZGVAYmxlbmhlaW1jaGFsY290LmNvbSIsInV0aSI6Ik9TWlNEM0RFWFVhYWRHRE1TWWg3QUEiLCJ2ZXIiOiIxLjAifQ.aJ6ZJ43VDYhqoSRtfntsVn5KREs3dyQ8PmHpqSJWEXMlTf1iZjchrkNwtfQgw5Iik08QwZnMw-tgt2VFS5OhDlT7YOnGLd4Z8ovWkxHrphHAvKI7WHtAf4umPl9OraIcn9ra4l0Hg9qm34p7XbVs_MZQ5OcihUfWdGuW5wX6Rdp4FSAFPSalk55spGQxyihQyntfuMOZTPx4AJdfM_pqEsoh3pq_bzp-TTnz8S5VykzUC7YTVxEpyJum9ZEoNsUkGhV2WuoRE2O5YKLfmsITcUVoh7UvkUMM4r9sHxVLg-o09HwESV0_xejmCOFUiaC-MtWDuttpzxbCtBS-kgZ5_A"
    #return access_token
    print(access_token)

def test_token_api_azure():
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