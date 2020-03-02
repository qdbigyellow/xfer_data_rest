from flask import Flask
from nordea_loan.get_rate_data_to_dashboard import loan_data_to_tsdb
from financial_modeling.company_data_to_tsdb import company_data_to_tsdb
from yr_weather.yr_weather_to_tsdb import yr_to_pg
from technical_analysis.bin.ta_to_dashboard import ta_pg

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello Hewen!"


@app.route("/getnordealoandata")
def transfer_data_to_dashboard():
    loan_data_to_tsdb()
    return "Get nordea loan data Done"


@app.route("/getfinancialfigures")
def transfer_finanical_data_to_dashboard():
    company_data_to_tsdb()
    return "Get financial data done"


@app.route("/yr")
def transfer_yrweather_data_to_dashboard():
    yr_to_pg()
    return "Get weather data done"


@app.route("/ta/<exec_idx>")
def transfer_ta_data_to_dashboard(exec_idx):
    # ta_to_dashboard(exec_idx)
    ta_pg(exec_idx)


if __name__ == '__main__':
    app.run()
