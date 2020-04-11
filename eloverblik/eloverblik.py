import requests
from os import path
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


METERS = {'H': '571313174114453369', 'V': '571313174113992944'}

def new_token():
    token_api = "https://api.eloverblik.dk/CustomerApi/api/Token"
    myfile = path.join(path.dirname(__file__), '1.txt')
    with open(myfile, 'r') as f:
        token = f.read()
    bearer_token = 'Bearer ' + token
    header = {"accept": "application/json", 'Authorization': bearer_token}
    r = requests.get(token_api, headers=header)
    new_token = r.json()['result'] if r.status_code == 200 else None
    return new_token


def read_time_series(token: str, meter: str = '571313174114453369', delta: int = 7, aggregation: str = 'Day'):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(delta)
    print(end_date)
    print(start_date)
    time_series_api = f'https://api.eloverblik.dk/CustomerApi/api/MeterData/GetTimeSeries/{start_date}/{end_date}/{aggregation}'
    bearer_token = 'Bearer ' + token
    headers = {"accept": "application/json", 'Authorization': bearer_token, 'Content-Type': 'application/json-patch+json'}
    body = '{ "meteringPoints": { "meteringPoint": [ "571313174114453369" ] } }'
    r = requests.post(time_series_api, headers=headers, data=body)
    return r.json()


def work_sheet(idx):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    #create some credential using that scope and content of startup_funding.json
    key = path.join(path.dirname(__file__),  "eng-particle-272612-d4c4113ddc86.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(key, scopes)
    #create gspread authorize using that credential
    client = gspread.authorize(creds)
    #Now will can access our google sheets we call client.open on StartupName
    sheet = client.open_by_key('1oYW4jK-ostUS5RJ-e4GGta7rN-W1rx4rGo6UQFhqYVg')
    #Access all of the record inside that
    worksheet = sheet.get_worksheet(idx)
    return worksheet

def read_eloverblik():
    token = new_token()
    resp = read_time_series(token)
    readings = resp["result"][0]["MyEnergyData_MarketDocument"]["TimeSeries"][0]["Period"]

    worksheet = work_sheet(0)
    worksheet.delete_rows(1, 100)
    for rd in readings:
        date = rd["timeInterval"]["end"]
        point = rd["Point"][0]["out_Quantity.quantity"]
        print(point)
        worksheet.append_row([date, point])

    resp = read_time_series(token, delta = 6 * 30, aggregation='Month')
    readings_month = resp["result"][0]["MyEnergyData_MarketDocument"]["TimeSeries"][0]["Period"]
    worksheet = work_sheet(1)
    worksheet.delete_rows(1,100)
    for rd in readings_month:
        date = rd["timeInterval"]["end"]
        point = rd["Point"][0]["out_Quantity.quantity"]
        print(point)
        worksheet.append_row([date, point])


if __name__ == "__main__":
    read_eloverblik()
