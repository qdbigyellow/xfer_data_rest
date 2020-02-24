import requests
import json
from technical_analysis.bin.indicator import Adx, Rsi, BBands
from typing import Sequence, Mapping
import numpy as np
import logging


class AlphaVantageSession:
    def __init__(self, apikey: str, host="www.alphavantage.co"):
        self.call_counter: int = 0
        self.HOST = host
        self.BASE_URL = f"http://{self.HOST}/query"
        self.APIKEY = apikey
        self.INTERVAL = "daily"
        self.SERIES_TYPE = "close"
        self.SESSION = self.create_session()
        self.LOGGER = self.create_logger()

    def create_logger(self):

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(f'{__name__}.log')
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        return logger

    def adx(self, symbol, adx: Adx, length=5):
        url = f"{self.BASE_URL}?function=adx&symbol={symbol}&interval={adx.interval}&time_period={adx.time_period}&series_type={adx.series_type}&apikey={self.APIKEY}"
        resp = self.get_json(url)
        if adx.data_key in resp.keys():
            j_data = resp[adx.data_key]
            self.LOGGER.info("ADX data received")
        else:
            self.LOGGER.warning("No ADX data received")
            return np.zeros(5)

        key_list = list(j_data.keys())[0:length]
        value_list = self.get_values(j_data, key_list, adx.key) 

        return np.array(value_list)

    def rsi(self, symbol, rsi: Rsi, length=5):
        url = f"{self.BASE_URL}?function=rsi&symbol={symbol}&interval={rsi.interval}&time_period={rsi.time_period}&series_type={rsi.series_type}&apikey={self.APIKEY}"
        j_data = self.get_json(url)[rsi.data_key]
        resp = self.get_json(url)
        if rsi.data_key in resp.keys():
            j_data = resp[rsi.data_key]
            self.LOGGER.info("RSI data received")
        else:
            self.LOGGER.warning("No RSI data received")
            return np.zeros(5)

        key_list = list(j_data.keys())[0:length]
        value_list = self.get_values(j_data, key_list, rsi.key) 

        return np.array(value_list)

    def bbands(self, symbol, bbands: BBands, length=5):
        url = f"{self.BASE_URL}?function=bbands&symbol={symbol}&interval={bbands.interval}&time_period={bbands.time_period}&series_type={bbands.series_type}&nbdevup={bbands.up}&nbdevdn={bbands.down}&apikey={self.APIKEY}"
        resp = self.get_json(url)
        if bbands.data_key in resp.keys():
            j_data = resp[bbands.data_key]
            self.LOGGER.info("BBands data received")
        else:
            self.LOGGER.warning("No BBands data received")
            return np.zeros(5)      
        key_list = list(j_data.keys())[0:length]
        value_list = self.get_values(j_data, key_list, bbands.key) 

        return np.array(value_list)

    def get_json(self, url):
        self.call_counter += 1
        resp = self.SESSION.get(url)
        return resp.json()
        
    def get_values(self, kv: Mapping[str, object], keys: Sequence[str], indicator_key: str) -> Sequence[str]:
        """give a dictionary, give a list of keys, return the value of the keys. 
           deeply couple with the data structure of Alpha-Vantage returned data.
        
        Args:
            kv (Mapping[str, object]): [description]
            keys (Sequence[str]): [a list of keys, normally the date]
            indicator_key (str): the key for the indicator 
        Returns:
            Sequence[str]: [a list of float values]
        """
        v_list = []
        for k in keys:
            # kv is a dict, kv[k] is also a dict, list(kv[k].values) converts the values to a list
            v = float(kv[k][indicator_key])
            v_list.append(v)
        return v_list

    def create_session(self):
        return requests.Session()
        
if __name__ == "__main__":
    av = AlphaVantageSession("9ADK2PQNQGTNB1NR")
    adx = Adx()
    d = av.adx("msft", adx)
    # e = av.rsi("msft")
    # f = av.bband("msft")
