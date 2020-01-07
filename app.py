from flask import Flask
from  nordea_loan.get_rate_data_to_dashboard import transfer_data_to_dashboard
from financial_modeling.company_data_to_tsdb import company_data_to_tsdb

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello Hewen!"

@app.route("/getnordealoandata")
def transfer_data_to_dashboard():
    transfer_data_to_dashboard()
    return "Get data Done"

@app.route("/getfinancialfigures")
def transfer_finanical_data_to_dashboard():
    company_data_to_tsdb()
    return "Get data done"

if __name__  == '__main__':
    app.run()
