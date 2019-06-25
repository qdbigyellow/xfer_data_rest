import json
import urllib.request as request

def fetch_data_to_gateway():
    for data in fetch_data():
        for loan in data:
            r = loan["rate"].replace("*&nbsp;", "").replace(",", ".")
            # print(r)
            af = loan["repaymentFreedomMax"]
            # if "*&nbsp;" in r:
            #    r = r.replace("*&nbsp;", "")
                # print(r)
            #if "," in r:
            #    r = r.replace(",", ".")
                # print(r)
            if float(r) < 100 and af.lower() == "nej":
                print(loan["loanPeriodMax"])
                print(r)

def fetch_data():
    result = json.load(request.urlopen("https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"))
    yield result

if __name__  == '__main__':
    fetch_data_to_gateway()