import json

import pytest
import requests



def test_count_page():
    url= "https://cms-stage.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:DESC&filters[$and][0][createdAt][$gt]=2024-02-27T18:30:00.000Z&filters[$and][1][conversationType][title][$eq]=Voice"
    payload={}
    headers = {
  'Accept': 'application/json',
  'Accept-Language': 'en-US,en;q=0.9',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImlhdCI6MTcwODM0MjUyNiwiZXhwIjoxNzEwOTM0NTI2fQ.5xe-EMX2RYePdrUhP_2rmBM7UfEjg22UmxZxxwIafxs',
  'Connection': 'keep-alive',
  'Cookie': '_clck=1l4b3wp%7C2%7Cfio%7C0%7C1484; _ga=GA1.2.187986154.1706094271; _ga_G6WKMM3SPZ=GS1.1.1706094271.1.1.1706094324.7.0.0',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    TCount = json_response["pagination"]["total"]
    print("Total record = "+str(TCount))
def test_succes_records():
    url1="https://cms-stage.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:DESC&filters[$and][0][createdAt][$gt]=2024-02-27T18:30:00.000Z&filters[$and][1][conversationType][title][$eq]=Voice&filters[$and][2][status][$eq]=success"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImlhdCI6MTcwODM0MjUyNiwiZXhwIjoxNzEwOTM0NTI2fQ.5xe-EMX2RYePdrUhP_2rmBM7UfEjg22UmxZxxwIafxs',
        'Connection': 'keep-alive',
        'Cookie': '_clck=1l4b3wp%7C2%7Cfio%7C0%7C1484; _ga=GA1.2.187986154.1706094271; _ga_G6WKMM3SPZ=GS1.1.1706094271.1.1.1706094324.7.0.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url1, headers=headers, data=payload)
    json_response = json.loads(response.text)
    SCount = json_response["pagination"]["total"]
    print("Total Report created " +str(SCount))

def test_transcribed_records():
    url1 = "https://cms-stage.comms-coach.englishscore.com/content-manager/collection-types/api::conversation.conversation?page=1&pageSize=10&sort=id:DESC&filters[$and][0][createdAt][$gt]=2024-02-27T18:30:00.000Z&filters[$and][1][conversationType][title][$eq]=Voice&filters[$and][2][status][$eq]=transcribed"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTUsImlhdCI6MTcwODM0MjUyNiwiZXhwIjoxNzEwOTM0NTI2fQ.5xe-EMX2RYePdrUhP_2rmBM7UfEjg22UmxZxxwIafxs',
        'Connection': 'keep-alive',
        'Cookie': '_clck=1l4b3wp%7C2%7Cfio%7C0%7C1484; _ga=GA1.2.187986154.1706094271; _ga_G6WKMM3SPZ=GS1.1.1706094271.1.1.1706094324.7.0.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url1, headers=headers, data=payload)
    json_response = json.loads(response.text)
    TCount = json_response["pagination"]["total"]
    print("Total Report Transcribed " + str(TCount))
