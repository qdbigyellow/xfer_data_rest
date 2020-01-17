import requests
from config import Configurations
from lxml import etree
from typing import Sequence, Mapping
from lib.tsdb.prom import push_data_to_gateway
from lib.pg_connector import conn, insert_query

def get_yr_data(url):
    location = Configurations.Endpoints.yr_weather[0]
    url = f"https://www.yr.no/place/{location}/forecast_hour_by_hour.xml"
    resp = requests.get(url)
    xml_data = etree.XML(resp.content)
    return xml_data


def forecast_to_pg(xml_data):
    place = Configurations.Endpoints.yr_weather[0].replace('/', '_')
    forecast_data = xml_data.xpath("//time")
    if len(forecast_data) > 0:
        connection = conn()
        for i, hourly_data in enumerate(forecast_data): 
            if i < Configurations.YR_Bashboard.lines:
                hours = f"next_{str(i)}"
                symbol = _xpath_search(hourly_data, "symbol").attrib['name']
                temperature = float(_xpath_search(hourly_data, "temperature").attrib['value'])
                windspeed = float(_xpath_search(hourly_data, "windSpeed").attrib['mps'])

                pg_insert_query = """INSERT INTO public.yr_forecast ("hours", "Weather", "Temperature", "WindSpeed") VALUES (%s,%s,%s,%s)
                                        ON CONFLICT ("hours")
                                        DO
                                            UPDATE 
                                            SET "Weather" = EXCLUDED."Weather",
                                            "Temperature" = EXCLUDED."Temperature",
                                            "WindSpeed" = EXCLUDED."WindSpeed"
                                        """
                record_to_insert = (hours, symbol, temperature, windspeed)
                insert_query(connection=connection, query=pg_insert_query, data=record_to_insert)
        connection.close()



def _xpath_search(xml_data, query):
    res = xml_data.xpath(query)
    if len(res) > 0:
        return res[0]

def yr_to_pg():
    xml_data = get_yr_data(Configurations.Endpoints.yr_weather)
    forecast_to_pg(xml_data)


#TODO: Delete all the code below that push data to TSDB    
def reformat_xml_data(xml_data):
    forecast_list: Sequence[Mapping[str, float]]  = []
    forecast_data = xml_data.xpath("//time")
    if len(forecast_data) > 0:
        for hourly_data in forecast_data:
            symbol = _xpath_search(hourly_data, "symbol")
            temperature = _xpath_search(hourly_data, "temperature")
            windspeed = _xpath_search(hourly_data, "windSpeed")
            hourly_dict = {
                symbol.tag: get_symbol(symbol),
                temperature.tag: float(temperature.attrib['value']),
                windspeed.tag: float(windspeed.attrib['mps'])
            }
            forecast_list.append(hourly_dict)
    return forecast_list

def forecast_to_tsdb(foracast_list):
    job_name = Configurations.YR_Bashboard.job_name
    for i in range(Configurations.YR_Bashboard.lines):
        labels = {
            'place': Configurations.Endpoints.yr_weather[0].replace('/', '_'),
            'hours': f"next_{str(i)}"
        }
        grouping_key = {
            'job': Configurations.YR_Bashboard.job_name, 
            'hours': f"next_{str(i)}"
        }
        for gauge, value in foracast_list[i].items():
            push_data_to_gateway(job_name=job_name, gauge_name=gauge, gauge_detail="see gauge name", data=value, labels=labels, grouping_key=grouping_key, pushadd=True)


def get_symbol(symbol_element) -> float:
    symbol_dict = {
        '1': 'Clear Sky',
        '2': 'Fair',
        '3': 'Partly Cloudy',
        '4': 'Cloudy',
        '9': 'Rain',
        '10': 'Heavy Rain',
        '15': 'Fog',
        '46': 'Light Rain'
    }

    num = symbol_element.attrib['numberEx']
    text = symbol_element.attrib['name']
    if not (num in symbol_dict.keys()):
        print(f"The number {num} is unknown")
        return 127.0

    if symbol_dict[num].lower() == text.lower():
        return float(num)
    else: 
        print(f"The number {num} is not mapped to text {text} anymore")
        return 127.0


def yr_to_tsdb():
    xml_data = get_yr_data(Configurations.Endpoints.yr_weather)
    data = reformat_xml_data(xml_data)
    forecast_to_tsdb(data)

