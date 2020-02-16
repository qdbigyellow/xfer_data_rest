import requests
from alpha_vantage_session import AlphaVantageSession
from indicator import Adx, Rsi, BBands
import time
from lib.pg_connector import conn, insert_query
import numpy as np
import os
import random


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
    "default": "FO1UZLB6BYAK9CYB"

}

SYMBOL_LIST = {
    "cn": SP500[0:165],
    "eu": SP500[166:331],
    "dk": SP500[332:],
    "default": get_non_sp500_symbols(150)
}


def truncate_ta_table(conn):
    cur = conn.cursor()
    cur.execute('truncate table ta')
    conn.commit()
    cur.execute('truncate table ta_overbuy')
    conn.commit()
    conn.close()




def ta_to_dashboard(exec_idx):
    db_ip = os.getenv("PG_HOST", "192.168.0.6")
    connection = conn(host=db_ip)

    if exec_idx.lower() == "truncate":
        truncate_ta_table(connection)
        return

    apikey = APIKEY.get(exec_idx, "FO1UZLB6BYAK9CYB")
    symbol_list = SYMBOL_LIST.get(exec_idx, get_non_sp500_symbols(length=150))

    adx = Adx()
    rsi = Rsi()
    bbands = BBands()
    av = AlphaVantageSession(apikey)



    symbol_list = ["msft", "aapl"]
    for s in symbol_list:
        if av.call_counter < 498:
            time.sleep(15) 
        else:
            break

        mkt_adx = av.adx(s, adx)
        if mkt_adx[0] < 30:
            continue
        time.sleep(15)

        mkt_rsi = av.rsi(s, rsi)
        if mkt_rsi[0] < 60:
            continue
        time.sleep(15)

        mkt_bbands = av.bbands(s, bbands)
        

        resp = requests.get(f"https://financialmodelingprep.com/api/v3/stock/real-time-price/{s}")
        price = resp.json()["price"]

        if mkt_bbands[0] < price and any(mkt_bbands > price) and 40 > np.average(mkt_adx) > 30 and 75 > np.average(mkt_adx) > 60 and np.average(mkt_adx[0:2]) > np.average(mkt_adx[2:4]) and np.average(mkt_rsi[0:2]) > np.average(mkt_rsi[2:4]):
            # Write the data to database
            pg_insert_query = """INSERT INTO public.ta ("symbol", "price", "adx", "rsi", "bbandshigh") VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (s, price, mkt_adx[0], mkt_rsi[0], mkt_bbands[0])
            insert_query(connection=connection, query=pg_insert_query, data=record_to_insert)
            connection.commit()

        if all(mkt_bbands < price) and np.average(mkt_adx) > 40 and np.average(mkt_rsi) > 75 and np.average(mkt_adx[0:2]) > np.average(mkt_adx[2:4]) and np.average(mkt_rsi[0:2]) > np.average(mkt_rsi[2:4]):
            # Write the data to database
            pg_insert_query = """INSERT INTO public.ta_overbuy ("symbol", "price", "adx", "rsi", "bbandshigh") VALUES (%s,%s,%s,%s,%s)"""
            record_to_insert = (s, price, mkt_adx[0], mkt_rsi[0], mkt_bbands[0])
            insert_query(connection=connection, query=pg_insert_query, data=record_to_insert)
            connection.commit()


    connection.close()

if __name__ == "__main__":
    ta_to_dashboard("cn")