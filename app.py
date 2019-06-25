from flask import Flask
import get_rate_data_to_dashboard 

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello Hewen!"

@app.route("/getdata")
def transfer_data_to_dashboard():
    get_rate_data_to_dashboard.transfer_data_to_dashboard()

if __name__  == '__main__':
    app.run()