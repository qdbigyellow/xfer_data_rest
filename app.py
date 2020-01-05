from flask import Flask
import get_rate_data_to_dashboard 
import stock_data_to_tsdb

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello Hewen!"

@app.route("/getnordealoandata")
def transfer_data_to_dashboard():
    get_rate_data_to_dashboard.transfer_data_to_dashboard()
    return "Get data Done"

@app.route("/getfinancialfigures")
def transfer_finanical_data_to_dashboard():
    stock_data_to_tsdb.main()
    return "Get data done"

if __name__  == '__main__':
    app.run()
