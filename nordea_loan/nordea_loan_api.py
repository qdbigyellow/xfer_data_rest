import json
import urllib.request as request
import re
from typing import List
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from os import path

nordea_kredit : List[str] = ["https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"]

def loan_sheet():
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    #create some credential using that scope and content of startup_funding.json
    key = path.join(path.dirname(__file__),  "eng-particle-272612-d4c4113ddc86.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(key, scopes)
    #create gspread authorize using that credential
    client = gspread.authorize(creds)
    #Now will can access our google sheets we call client.open on StartupName
    sheet = client.open_by_key('13KRQpK1iaeqY9-lm0Phw9yEP5Vjxxx9L4EC-_250gvA')
    #Access all of the record inside that
    worksheet = sheet.get_worksheet(0)
    result = worksheet.get_all_values()
    print(result)
    return result


def work_sheet(idx):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    #create some credential using that scope and content of startup_funding.json
    key = path.join(path.dirname(__file__),  "eng-particle-272612-d4c4113ddc86.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(key, scopes)
    #create gspread authorize using that credential
    client = gspread.authorize(creds)
    #Now will can access our google sheets we call client.open on StartupName
    sheet = client.open_by_key('13KRQpK1iaeqY9-lm0Phw9yEP5Vjxxx9L4EC-_250gvA')
    #Access all of the record inside that
    worksheet = sheet.get_worksheet(idx)
    return worksheet


def loan_data_to_tsdb():
    rates = []
    for data in fetch_data():
        print(f"{len(data)} is fetched")
        if len(data) > 0 and "rate" in data[0]:
            rates = process_loan_rate_data(data)      
    return rates

def fetch_data():
    # for l in Configurations.Endpoints.nordea_kredit:
    for l in nordea_kredit:
        result = json.load(request.urlopen(l))
        yield result

def process_loan_rate_data(data):
    rates = []
    worksheet = work_sheet(0)
    worksheet.delete_rows(1, 100)
    worksheet.append_row(["Loan Type", "Rate"])
    for loan in data:
        name = "nordea_loan"
        rate = loan["rate"].replace("*&nbsp;", "").replace(",", ".")
        afdragsfri = loan["repaymentFreedomMax"]
        loan_type = "loan_" + loan["fundName"].replace(" ", "_").replace(",", "_").replace("%", "_").replace("__", "_").lower()        
        labels = {
            "loan_type": loan_type
        }
        grouping_key = {
            "job": name,            
            "loan_type": loan_type
        }
        period = loan["loanPeriodMax"]
        print(f"matrics {name}")

        if float(rate) < 100 and afdragsfri.lower() == "nej":
            rates.append(rate)
            worksheet.append_row([loan_type, rate])
    return rates

def replace_non_alphanumeric(data):
    pattern= re.compile(r'\W+')
    pattern.sub('_', data)    
    

if __name__ == "__main__":
    loan_data_to_tsdb()