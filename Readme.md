# Purpose
This Repo contains a Flask web server, and few python modules, which could get the data from external endpoint, reformat them, push to TSDB (Prometheus) , and finnaly displayed on Dashboard (Grafana). 

The dashboard is used at home. 

The web server is running in a docker, a cron job is regularlly calling the endpoints. 

## How to start the container
docker run --name app -p 5000:5000/tcp --network="99f1c" -v /home/admin/xfer_data_rest:/app <imageId>

## Data Source
* Nordea Loan Data
https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json

* Financial data is sponsed by 
https://financialmodelingprep.com/developer/docs

* YR Weather data
https://www.yr.no/place/Denmark/Capital/Hellerup//forecast_hour_by_hour.xml
