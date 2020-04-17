import json
import urllib.request as request
import re
from typing import List
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from os import path

nordea_kredit: List[str] = [
    "https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"]


def loan_reate_to_gspread():
    rates = []
    for data in fetch_data():
        print(f"{len(data)} is fetched")
        if len(data) > 0 and "rate" in data[0]:
            rates = process_loan_rate_data(data)
    return rates


def work_sheet(id: str, idx: int):
    """Open the google spreadsheet by id. 
       and return the worksheet by index 
    Args:
        id (str): [The id of google spreadsheet]
        idx (int): [The index of sheet]

    Returns:
        [gspread.models.Worksheet]: [A worksheet object]
    """
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive']
    # create some credential using that scope and content of startup_funding.json
    key = path.join(path.dirname(__file__),
                    "eng-particle-272612-d4c4113ddc86.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(key, scopes)
    # create gspread authorize using that credential
    client = gspread.authorize(creds)
    # Now will can access our google sheets we call client.open on StartupName
    sheet = client.open_by_key(id)
    # Access all of the record inside that
    worksheet = sheet.get_worksheet(idx)
    return worksheet


def fetch_data():
    # for l in Configurations.Endpoints.nordea_kredit:
    for l in nordea_kredit:
        result = json.load(request.urlopen(l))
        yield result


def process_loan_rate_data(data):
    rates = []
    worksheet = work_sheet('13KRQpK1iaeqY9-lm0Phw9yEP5Vjxxx9L4EC-_250gvA', 0)
    worksheet.delete_rows(2, worksheet.row_count + 1)
    for loan in data:
        name = "nordea_loan"
        rate = loan["rate"].replace("*&nbsp;", "").replace(",", ".")
        afdragsfri = loan["repaymentFreedomMax"]
        loan_type = "loan_" + loan["fundName"].replace(" ", "_").replace(
            ",", "_").replace("%", "_").replace("__", "_").lower()

        print(f"matrics {name}")

        if float(rate) < 100 and afdragsfri.lower() == "nej":
            rates.append(rate)
            worksheet.append_row([loan_type, rate])
    return rates


if __name__ == "__main__":
    loan_reate_to_gspread()
