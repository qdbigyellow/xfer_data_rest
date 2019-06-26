from config import Configurations
import json
import urllib.request as request
from lib.tsdb.prom import push_data_to_gateway

def transfer_data_to_dashboard():
    for data in fetch_data():
        if len(data) > 0 and "rate" in data[0]:
            process_loan_rate_data(data)        

def fetch_data():
    for l in Configurations.Server.dest:
        result = json.load(request.urlopen(l))
        yield result

def process_loan_rate_data(data):
    for loan in data:
        rate = loan["rate"].replace("*&nbsp;", "").replace(",", ".")
        afdragsfri = loan["repaymentFreedomMax"]
        name = "loan" + loan["fundName"].replace(" ", "_").replace(",", "_").replace("%", "_").replace("__", "_").lower()
        period = loan["loanPeriodMax"]

        if float(rate) < 100 and afdragsfri.lower() == "nej":
            push_data_to_gateway(job_name="Nordea Loan", gauge_name=name, gauge_detail=period, data=rate)
