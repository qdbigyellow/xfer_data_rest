import requests
from config import Configurations
from lxml import etree
from typing import Sequence, Mapping
from lib.tsdb.prom import push_data_to_gateway


def get_yr_data(url):
    location = Configurations.Endpoints.yr_weather[0]
    url = f"https://www.yr.no/place/{location}/forecast_hour_by_hour.xml"
    resp = requests.get(url)
    xml_data = etree.XML(resp.content)
    return xml_data

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
            'place': Configurations.Endpoints.yr_weather[0],
            'hours': f"+{str(i)}"
        }
        grouping_key = {
            'job': Configurations.YR_Bashboard.job_name, 
            'place': Configurations.Endpoints.yr_weather[0]
        }
        for gauge, value in foracast_list[i].items():
            push_data_to_gateway(job_name=job_name, gauge_name=gauge, gauge_detail="see gauge name", data=value, labels=labels, grouping_key=grouping_key, pushadd=True)



def _xpath_search(xml_data, query):
    res = xml_data.xpath(query)
    if len(res) > 0:
        return res[0]

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
        print(f"The number {number} is unknown")
        return 127.0

    if symbol_dict[num].lower() == text.lower():
        return float(num)
    else: 
        print(f"The number {number} is not mapped to text {text} anymore")
        return 127.0


def yr_to_tsdb():
    xml_data = get_yr_data(Configurations.Endpoints.yr_weather)
    data = reformat_xml_data(xml_data)
    forecast_to_tsdb(data)
