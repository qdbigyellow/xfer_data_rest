from config import Configurations
import json
import urllib.request as request
from lib.tsdb.prom import push_data_to_gateway
import re

def loan_data_to_tsdb():
    for data in fetch_data():
        print(f"{len(data)} is fetched")
        if len(data) > 0 and "rate" in data[0]:
            process_loan_rate_data(data)        

def fetch_data():
    for l in Configurations.Endpoints.nordea_kredit:
        result = json.load(request.urlopen(l))
        yield result

def process_loan_rate_data(data):
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
            push_data_to_gateway(job_name=name, gauge_name="nordea_loan_rate", gauge_detail=period, data=rate, labels=labels, grouping_key=grouping_key, pushadd=True)

def replace_non_alphanumeric(data):
    pattern= re.compile(r'\W+')
    pattern.sub('_', data)    
    
