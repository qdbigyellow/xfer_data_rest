import requests
from technical_analysis.bin.alpha_vantage_session import AlphaVantageSession
from technical_analysis.bin.indicator import Adx, Rsi, BBands
import time
from lib.pg_connector import conn, insert_query
import numpy as np
import os
import random
import logging

SP500 = ['AAPL', 'ABT', 'ABBV', 'ACN', 'ACE', 'ADBE', 'ADT', 'AAP', 'AES', 'AET', 'AFL',
'AMG', 'A', 'GAS', 'ARE', 'APD', 'AKAM', 'AA', 'AGN', 'ALXN', 'ALLE', 'ADS', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVGO', 'AVB', 'AVY', 'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BXLT', 'BAX', 'BBT', 'BDX', 'BBBY', 'BRK.B', 'BBY', 'BLX', 'HRB', 'BA', 'BWA', 'BXP', 'BSX', 'BMY', 'BRCM', 'BF.B', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'HSIC', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CMG', 'CB', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'GLW', 'COST', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DLPH', 'DAL', 'XRAY', 'DVN', 'DO', 'DTV', 'DFS', 'DISCA', 'DISCK', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMC', 'EMR', 'ENDP', 'ESV', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'EXC', 'EXPE', 'EXPD', 'ESRX', 'XOM', 'FFIV', 'FB', 'FAST', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FOSL', 'BEN', 'FCX', 'FTR', 'GME', 'GPS', 'GRMN', 'GD', 'GE', 'GGP', 'GIS', 'GM', 'GPC', 'GNW', 'GILD', 'GS', 'GT', 'GOOGL', 'GOOG', 'GWW', 'HAL', 'HBI', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCA', 'HCP', 'HCN', 'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'ITW', 'IR', 'INTC', 'ICE', 'IBM', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IRM', 'JEC', 'JBHT', 'JNJ', 'JCI', 'JOY', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'GMCR', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS', 'KRFT', 'KR', 'LB', 'LLL', 'LH', 'LRCX', 'LM', 'LEG', 'LEN', 'LVLT', 'LUK', 'LLY', 'LNC', 'LLTC', 'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MNK', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MJN', 'MMV', 'MDT', 'MRK', 'MET', 'KORS', 'MCHP', 'MU', 'MSFT', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MUR', 'MYL', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NFLX', 'NWL', 'NFX', 'NEM', 'NWSA', 'NEE', 'NLSN', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NRG', 'NUE', 'NVDA', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'PLL', 'PH', 'PDCO', 'PAYX', 'PNR', 'PBCT', 'POM', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PBI', 'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RTN', 'O', 'RHT', 'REGN', 'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RLD', 'R', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'STX', 'SEE', 'SRE', 'SHW', 'SPG', 'SWKS', 'SLG', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'STI', 'SYMC', 'SYY', 'TROW', 'TGT', 'TEL', 'TE', 'TGNA', 'THC', 'TDC', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TJX', 'TMK', 'TSS', 'TSCO', 'RIG', 'TRIP', 'FOXA', 'TSN', 'TYC', 'UA', 'UNP', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VRTX', 'VIAB', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'ANTM', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WFM', 'WMB', 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YHOO', 'YUM', 'ZBH', 'ZION', 'ZTS']

def get_non_sp500_symbols(length:int=150):
    resp = requests.get("https://financialmodelingprep.com/api/v3/company/stock/list")
    all_list = resp.json()["symbolsList"]
    s_list = []
    for s in all_list:
        if "name" not in s.keys():
            continue

        if "fund" in s["name"].lower():
            continue

        if "ishare" in s["name"].lower():
            continue

        if "proshare" in s["name"].lower():
            continue

        if "vanguard" in s["name"].lower():
            continue

        if "etf" in s["name"].lower():
            continue

        if ("NASDAQ" in s["exchange"] or "York" in s["exchange"]) and ("inc" in s["name"].lower() or "corporation" in s["name"].lower() or "limited" in s["name"].lower()):
            s_list.append(s["symbol"])

    if len(s_list) < length:
        return s_list

    ind = random.randint(0, len(s_list)-length)
    return s_list[ind: ind+length-1]

APIKEY = {
    "cn": "BEWAMFQCP8QX3R8D", 
    "eu": "2P0DJRUU9I3A25K8",
    "dk": "9ADK2PQNQGTNB1NR",
    "default": "FO1UZLB6BYAK9CYB",
    "worldtradingdata": "rzjynzyO8kiiVNvUlTcaJE0S2r8e2c2fy97GJu5GmssKIBAFbu7SK1wJGGfi"

}

SYMBOL_LIST = {
    "cn": SP500[0:165],
    "eu": SP500[166:331],
    "dk": SP500[332:],
    "default": get_non_sp500_symbols(150)
}



def create_logger():

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


LOGGER = create_logger()

def truncate_ta_table(connection):
    pg_insert_query = """truncate table ta"""
    insert_query(connection, query=pg_insert_query, data=None)
    LOGGER.info("table ta truncated")
    pg_insert_query = """truncate table ta_overbuy"""
    insert_query(connection, query=pg_insert_query, data=None)
    LOGGER.info("table ta_overbuy truncated")
    connection.close()


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.adx = None
        self.rsi = None
        self.BBands = None
        self.ADX_Level1 = 30
        self.ADX_Level2 = 50
        self.RSI_Level1 = 65
        self.RSI_Level2 = 80
        

    def strong_up(self):
        return all(self.bbands < self.price) and \
                np.average(self.bbands[0:2]) > np.average(self.bbands[2:4]) and \
                self.ADX_Level2 > np.average(self.adx) > self.ADX_Level1 and \
                self.RSI_Level2 > np.average(self.rsi) > self.RSI_Level1 and \
                np.average(self.adx[0:2]) > np.average(self.adx[2:4]) and \
                np.average(self.rsi[0:2]) > np.average(self.rsi[2:4])

    def overbuy(self):
        return all(self.bbands < self.price) and \
                np.average(self.adx) > self.ADX_LEVEL2 and \
                np.average(self.rsi) > self.ADX_LEVEL2 and \
                np.average(self.adx[0:2]) > np.average(self.adx[2:4]) and \
                np.average(self.rsi[0:2]) > np.average(self.rsi[2:4])

class Engine:
    def __init__(self, db_ip="192.168.0.6", action="cn"):
        self.db_ip = os.getenv("PG_HOST", db_ip)       
        self.ta_table = "ta"
        self.overbuy_table = "ta_overbuy"
        self.LOGGER = create_logger()
        self.action = action
        self.apikey = APIKEY.get(action)
        self.symbol_list = SYMBOL_LIST.get(action, get_non_sp500_symbols(length=150))
        self.adx = Adx()
        self.rsi = Rsi()
        self.bbands = BBands()
        self.av = AlphaVantageSession(self.apikey)


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

    
    def request_json(self, url):
        resp = requests.get(url)
        return resp.json()

    def exeucte(self, stock):
        self.LOGGER.info(f"reading information for {stock.symbol}")
        if self.av.call_counter < 498:
            self.LOGGER.info(f"current call counter {self.av.call_counter}")
            time.sleep(15) 
        else:
            return

        stock.adx = self.av.adx(stock.symbol, self.adx)
        self.LOGGER.info(f"current ADX {stock.adx}")
        if stock.adx < 30:
            return
        time.sleep(15)

        stock.rsi = self.av.rsi(stock.symbol, self.rsi)
        self.LOGGER.info(f"current RSI {stock.rsi}")
        if stock.rsi[0] < 60:
            return
        time.sleep(15)

        stock.BBands = self.av.bbands(stock.symbol, self.bbands)
        self.LOGGER.info(f"current BBbands {stock.BBands}")
        
        data = self.request_json(url=f"https://financialmodelingprep.com/api/v3/stock/real-time-price/{stock.symobl}")
        if not "price" in data.keys():
            self.LOGGER.warning("No Price information available from financialmodelingprep.com")
            n_data = self.request_json(url=f"https://api.worldtradingdata.com/api/v1/stock?symbol={stock.symbol}&api_token={APIKEY.get('worldtradingdata')}")
            if "data" in n_data.keys():
                data=float(data["data"][0])
                self.LOGGER.infoI("get data from worldtradingdata.com")
            else:
                self.LOGGER.warning("No Price information available from worldtradingdata.com")
                return
        
        price = data["price"]
        if price is None:
            self.LOGGER.warning("No Price is None")
            return
        else:           
            stock.price = float(price)
            self.LOGGER.info(f"current price {stock.price}")

        if stock.strong_up(self):
            self.update_table(self.ta_table)

        if stock.overbuy(self):
            self.update_table(self.overbuy)


    def truncate_table(self, table):
        db_conn = conn(host=self.db_ip)
        pg_insert_query = f"""truncate table {table}"""
        insert_query(self.db_conn, query=pg_insert_query, data=None)
        self.LOGGER.info(f"table {table} truncated")
        db_conn.close()


    def update_table(self, stock, table):
        db_conn = conn(host=self.db_ip)
        pg_insert_query = f"""INSERT INTO public.{table} ("symbol", "price", "adx", "rsi", "bbandshigh") VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (stock.symbol, stock.price, stock.adx[0], stock.rsi[0], stock.bbands[0])
        insert_query(connection=db_conn, query=pg_insert_query, data=record_to_insert)
        self.LOGGER.info(f"update {table} table")

        db_conn.close()

def ta_pg(exec_idx):
    engine = Engine(action=exec_idx)
    if exec_idx.lower() == "truncate":
        engine.truncate_table(engine.ta_table)
        engine.truncate_table(engine.overbuy)
        return

    for s in engine.symbo_list:
        stock = Stock(symbol=s)
        engine.exeucte(stock=stock)          


def ta_to_dashboard(exec_idx):
    db_ip = os.getenv("PG_HOST", "192.168.0.6")
    connection = conn(host=db_ip)

    if exec_idx.lower() == "truncate":
        truncate_ta_table(connection)
        LOGGER.info("Database truncated")
        return

    apikey = APIKEY.get(exec_idx, "FO1UZLB6BYAK9CYB")
    symbol_list = SYMBOL_LIST.get(exec_idx, get_non_sp500_symbols(length=150))
    LOGGER.info(f"use execution index {exec_idx}")

    adx = Adx()
    rsi = Rsi()
    bbands = BBands()
    av = AlphaVantageSession(apikey)
    for s in symbol_list:
        LOGGER.info(f"reading information for {s}")
        if av.call_counter < 498:
            LOGGER.info(f"current call counter {av.call_counter}")
            time.sleep(15) 
        else:
            break

        mkt_adx = av.adx(s, adx)
        LOGGER.info(f"current ADX {mkt_adx}")
        if mkt_adx[0] < 30:
            continue
        time.sleep(15)

        mkt_rsi = av.rsi(s, rsi)
        LOGGER.info(f"current RSI {mkt_rsi}")
        if mkt_rsi[0] < 60:
            continue
        time.sleep(15)

        mkt_bbands = av.bbands(s, bbands)
        LOGGER.info(f"current BBbands {mkt_bbands}")
        

        resp = requests.get(f"https://financialmodelingprep.com/api/v3/stock/real-time-price/{s}")
        data = resp.json()
        if not "price" in data.keys():
            LOGGER.warning("No Price information available from financialmodelingprep.com")

            resp = requests.get(f"https://api.worldtradingdata.com/api/v1/stock?symbol={s}&api_token={APIKEY.get('worldtradingdata')}")
            n_data = resp.json()
            if "data" in n_data.keys():
                data=float(data["data"][0])
                LOGGER.infoI("get data from worldtradingdata.com")
            else:
                LOGGER.warning("No Price information available from worldtradingdata.com")
                continue 
        
        price = data["price"]
        if price is None:
            LOGGER.warning("No Price is None")
            continue
        else:           
            price = float(price)
            LOGGER.info(f"current price {price}")
        if all(mkt_bbands < price) and np.average(mkt_bbands[0:2]) > np.average(mkt_bbands[2:4]) and 40 > np.average(mkt_adx) > 30 and 75 > np.average(mkt_rsi) > 60 and np.average(mkt_adx[0:2]) > np.average(mkt_adx[2:4]) and np.average(mkt_rsi[0:2]) > np.average(mkt_rsi[2:4]):
            # Write the data to database
            pg_insert_query = """INSERT INTO public.ta ("symbol", "price", "adx", "rsi", "bbandshigh") VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (s, price, mkt_adx[0], mkt_rsi[0], mkt_bbands[0])
            insert_query(connection=connection, query=pg_insert_query, data=record_to_insert)
            LOGGER.info(f"update ta table")

        if all(mkt_bbands < price) and np.average(mkt_adx) > 40 and np.average(mkt_rsi) > 75 and np.average(mkt_adx[0:2]) > np.average(mkt_adx[2:4]) and np.average(mkt_rsi[0:2]) > np.average(mkt_rsi[2:4]):
            # Write the data to database
            pg_insert_query = """INSERT INTO public.ta_overbuy ("symbol", "price", "adx", "rsi", "bbandshigh") VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (s, price, mkt_adx[0], mkt_rsi[0], mkt_bbands[0])
            insert_query(connection=connection, query=pg_insert_query, data=record_to_insert)
            LOGGER.info(f"update ta_overbuy table")
            
    connection.close()

if __name__ == "__main__":
    ta_to_dashboard("cn")