#%%
from config import Configurations
import json
import requests
from lib.tsdb.prom import push_data_to_gateway
import re
from typing import Mapping
from financial_modeling.company_figures import CompanyFigures
from collections import defaultdict
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from dataclasses import dataclass

def gauge_dict():
    g_dict = defaultdict(lambda: "see gauge name")
    g_dict['gross_profit_growth'] = "Gross Profit Groth"
    g_dict['pb_ratio'] = "Share price to Book value. Less than one means share is under valued"
    return g_dict

G_DICT = gauge_dict()

def get_remote_data(symbol: str, report: str, period: str ='quarter'):
    url = f'https://financialmodelingprep.com/api/v3/{report}/{symbol}?period={period}'
    resp = requests.get(url)
    jdata = resp.json()
    return jdata

def get_symbol_list():
    url = 'https://financialmodelingprep.com/api/v3/company/stock/list'
    resp = requests.get(url)
    jdata = resp.json()
    symbol_list = [j['symbol'] for j in jdata['symbolsList']]
    return symbol_list

def assemble_data():
    pass

def push_figures_to_db(figures: CompanyFigures):
    for k, v in vars(figures).items():
        if not (k == 'name' or k == 'date'):
            gauge_detail = G_DICT[k]
            push_to_db(k, v, figures.name, figures.date, gauge_detail)

def push_to_db(name, data, symbol, date, gauge_detail):
    job_name = f"finanical_statement"
    labels = {
        'symbol': symbol, 
        'date': date
    } 

    grouping_key = {
        'job': job_name,
        'symbol': symbol
    }
    push_data_to_gateway(job_name=job_name, gauge_name=name, gauge_detail="see gauge name", data=data, labels=labels, grouping_key=grouping_key, pushadd=True)


def get_data(symbol: str, period='quarter'):
    """
    Iterate the report type, and get the data from the remote endpoint.  
    Output is a dictionary, where the key is the report type, and the value is a json data.
    """
    dataset = {}
    for t in Configurations.Endpoints.finanical_modeling:
        dataset[t] = get_remote_data(symbol=symbol, report=t)
    return dataset


def last_timestamp(data):
    """
    Get the last timestamp of each finanical report. 
    """
    last_ts = {}
    last_ts['balance_sheet'] = data['financials/balance-sheet-statement']['financials'][0]["date"]
    last_ts['income'] = data['financials/income-statement']['financials'][0]["date"]
    last_ts['cash_flow'] = data['financials/cash-flow-statement']['financials'][0]["date"]
    last_ts['company_key_metrics'] = data['company-key-metrics']['metrics'][0]["date"]
    last_ts['finacial_growth'] = data['financial-statement-growth']['growth'][0]["date"]
    last_ts['enterprise_value'] = data['enterprise-value']['enterpriseValues'][0]["date"]
    last_ts['financial_ratios'] = data['financial-ratios']['ratios'][0]["date"]
    return last_ts

def min_index(data):
    return min(len(data['financials/balance-sheet-statement']['financials']), len(data['financials/income-statement']['financials']), 
               len(data['financials/cash-flow-statement']['financials']), len(data['company-key-metrics']['metrics']),
               len(data['financial-statement-growth']['growth']), len(data['enterprise-value']['enterpriseValues']), len(data['financial-ratios']['ratios']))

def new_data(last_ts):
    return True

def new_company(symbol: str):
    compnay_folder = os.path.join(os.path.abspath(__file__), "timestamp") 
    return symbol not in os.listdir(compnay_folder)        

def add_data(report: str, data: dict, figures: CompanyFigures, index: int = 0):
    """
    Add data to CompanyFigures data class
    Args:
        report: report is name of report (a.k.a the name used in endpoint)
        data: the data received from endpoint
        figures: CompanyFigures object
        index: the data is in a json array, the index number indicate which data set should be used. Normally only the latest data is used(index=0)
    Returns:
        A CompanyFigures object with data
    """
    symbol_keys = SupportKeys()
    # TODO:  the path depends on the matrix,  so no need for check report name
    try:
        if report == 'financial-statement-growth':
            if index < len(data['growth']):
                figures.date = data['growth'][index]["date"]
                figures.gross_profit_growth = float(data['growth'][index][symbol_keys.gross_profit_growth.value])
                figures.ebit_growth = float(data['growth'][index][symbol_keys.ebit_growth.value])
                figures.operating_income_growth = float(data['growth'][index][symbol_keys.operating_income_growth.value])
                figures.net_income_growth = float(data['growth'][index][symbol_keys.net_income_growth.value])
                figures.eps_growth = float(data['growth'][index][symbol_keys.eps_growth.value])
                figures.eps_diluted_growth = float(data['growth'][index][symbol_keys.eps_diluted_growth.value])
                figures.weighted_average_shares_growth = float(data['growth'][index][symbol_keys.weighted_average_shares_growth])
                figures.weighted_average_shares_diluted_growth = float(data['growth'][index][symbol_keys.weighted_average_shares_diluted_growth.value])
                figures.divident_per_share_growth = float(data['growth'][index][symbol_keys.divident_per_share_growth.value])
                figures.operating_cash_flow_growth = float(data['growth'][index][symbol_keys.operating_cash_flow_growth.value])
                figures.free_cash_flow_growth = float(data['growth'][index][symbol_keys.free_cash_flow_growth.value])
                figures.receivables_growth = float(data['growth'][index][symbol_keys.receivables_growth.value])
                figures.inventory_growth = float(data['growth'][index][symbol_keys.inventory_growth.value])
                figures.asset_growth = float(data['growth'][index][symbol_keys.asset_growth.value])
                figures.book_value_per_share_growth = float(data['growth'][index][symbol_keys.book_value_per_share_growth.value])
                figures.debt_growth = float(data['growth'][index][symbol_keys.debt_growth.value])
                figures.rd_expense_growth = float(data['growth'][index][symbol_keys.rd_expense_growth.value])
                figures.sga_expense_growth = float(data['growth'][index][symbol_keys.sga_expense_growth.value])
        elif report == 'financials/income-statement':
            if index < len(data['financials']):
                figures.ops_expense_to_income_ratio = float(data['financials'][index][symbol_keys.operating_expense.value])/float(data['financials'][index][symbol_keys.operating_income.value])
                if len(data) > index + 1:
                    figures.ops_expense_growth = float(data['financials'][index][symbol_keys.operating_expense.value]) / float(data['financials'][index+1][symbol_keys.operating_expense.value])
        elif report == 'financials/balance-sheet-statement':
            if index < len(data['financials']):
                figures.short_term_debt_to_total_ratio = float(data['financials'][index][symbol_keys.shortterm_debt.value]) / float(data['financials'][index][symbol_keys.total_debt.value])
                figures.asset_to_liability_ratio = float(data['financials'][index][symbol_keys.total_asset.value]) / float(data['financials'][index][symbol_keys.total_liabilities.value])
        elif report == 'company-key-metrics':
            if index < len(data['metrics']):
                figures.pe_ratio = float(data['metrics'][index][symbol_keys.pe_ratio.value])
                figures.pb_ratio = float(data['metrics'][index][symbol_keys.pb_ratio.value])
        elif report == 'company/rating':
            rating_details = []
            for r, w in data['ratingDetails'].items():
                rating_details.append(float(w["score"]))
            figures.rating = sum(rating_details) / len(rating_details)
    except Exception:
        pass



def generate_tsdb_data(symbol:str, data: dict, index: int=0):
    # TODO in Python 3.7, the order of insertion to dictionary is maintained, so it is possible to use a position index to get the symbol
    # so don't need the hardcoded dictionary key.
    # https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary/39292086
    figures = CompanyFigures(symbol)
    for k, v in data.items():
        add_data(k, v, figures, index)
    return figures

def company_data_to_tsdb():
    # Push the data to TSDB.  Only push the latest data into TSDB.  To analysis the history data, use python code instead 
    # Args:
    symbols = get_symbol_list()
    symbols = ['aapl', 'msft', 'fds']
    for symbol in symbols:
        f_data = get_data(symbol)
        figures = generate_tsdb_data(symbol, f_data, 0)
        # push_figures_to_db(figures)
        print(figures)



def get_company_growth(symbol):
    symbol_keys = SupportKeys()
    growth_report = Configurations.Endpoints.finanical_modeling[6]
    data = get_remote_data(symbol, growth_report)
    growth_data = pd.DataFrame()
    company_growth = {}
    company_growth["Date"] = []
    company_growth[symbol_keys.gross_profit_growth.value] = []
    company_growth[symbol_keys.ebit_growth.value] = []
    company_growth[symbol_keys.operating_income_growth.value] = []
    company_growth[symbol_keys.net_income_growth.value] = []
    company_growth[symbol_keys.eps_growth.value] = []
    company_growth[symbol_keys.divident_per_share_growth.value] = []
    company_growth[symbol_keys.operating_cash_flow_growth.value] = []
    company_growth[symbol_keys.free_cash_flow_growth.value] = []
    company_growth[symbol_keys.receivables_growth.value] = []
    company_growth[symbol_keys.asset_growth.value] = []
    company_growth[symbol_keys.book_value_per_share_growth.value] = []
    company_growth[symbol_keys.debt_growth.value] = []
    company_growth[symbol_keys.rd_expense_growth.value] = []
    company_growth[symbol_keys.sga_expense_growth.value] = []

    for d in data["growth"]:
        company_growth["Date"].append(d["date"])
        company_growth[symbol_keys.gross_profit_growth.value].append(float(d[symbol_keys.gross_profit_growth.value])) 
        company_growth[symbol_keys.ebit_growth.value].append(float(d[symbol_keys.ebit_growth.value]))
        company_growth[symbol_keys.operating_income_growth.value].append(float(d[symbol_keys.operating_income_growth.value]))
        company_growth[symbol_keys.net_income_growth.value].append(float(d[symbol_keys.net_income_growth.value]))
        company_growth[symbol_keys.eps_growth.value].append(float(d[symbol_keys.eps_growth.value]))
        company_growth[symbol_keys.divident_per_share_growth.value].append(float(d[symbol_keys.divident_per_share_growth.value]))
        company_growth[symbol_keys.operating_cash_flow_growth.value].append(float(d[symbol_keys.operating_cash_flow_growth.value]))
        company_growth[symbol_keys.free_cash_flow_growth.value].append(float(d[symbol_keys.free_cash_flow_growth.value]))
        company_growth[symbol_keys.receivables_growth.value].append(float(d[symbol_keys.receivables_growth.value]))
        company_growth[symbol_keys.asset_growth.value].append(float(d[symbol_keys.asset_growth.value]))
        company_growth[symbol_keys.book_value_per_share_growth.value].append(float(d[symbol_keys.book_value_per_share_growth.value]))
        company_growth[symbol_keys.debt_growth.value].append(float(d[symbol_keys.debt_growth.value]))
        company_growth[symbol_keys.rd_expense_growth.value].append(float(d[symbol_keys.rd_expense_growth.value]))
        company_growth[symbol_keys.sga_expense_growth.value].append(float(d[symbol_keys.sga_expense_growth.value]))
    company_growth_data = pd.DataFrame.from_dict(company_growth)
    company_growth_data.set_index("Date", inplace=True)
    return company_growth_data

@dataclass
class Keys:
    report: str
    path: str
    value: str

class SupportKeys:
    date = Keys('financial-statement-growth', 'growth', "date")
    gross_profit_growth = Keys('financial-statement-growth', 'growth', "Gross Profit Growth")
    ebit_growth = Keys('financial-statement-growth', 'growth', "EBIT Growth")
    operating_income_growth = Keys('financial-statement-growth', 'growth', "Operating Income Growth")
    net_income_growth = Keys('financial-statement-growth', 'growth', "Net Income Growth")
    eps_growth = Keys('financial-statement-growth', 'growth', "EPS Growth")
    eps_diluted_growth = Keys('financial-statement-growth', 'growth', "EPS Diluted Growth")
    weighted_average_shares_growth = Keys('financial-statement-growth', 'growth', "Weighted Average Shares Growth")
    weighted_average_shares_diluted_growth = Keys('financial-statement-growth', 'growth', "Weighted Average Shares Diluted Growth")
    divident_per_share_growth = Keys('financial-statement-growth', 'growth', "Dividends per Share Growth")
    operating_cash_flow_growth = Keys('financial-statement-growth', 'growth', "Operating Cash Flow growth")
    free_cash_flow_growth = Keys('financial-statement-growth', 'growth', "Free Cash Flow growth")
    receivables_growth = Keys('financial-statement-growth', 'growth', "Receivables growth")
    inventory_growth = Keys('financial-statement-growth', 'growth', "Inventory Growth")
    asset_growth = Keys('financial-statement-growth', 'growth', "Asset Growth")
    book_value_per_share_growth = Keys('financial-statement-growth', 'growth', "Book Value per Share Growth")
    debt_growth = Keys('financial-statement-growth', 'growth', "Debt Growth")
    rd_expense_growth = Keys('financial-statement-growth', 'growth', "R&D Expense Growth")
    sga_expense_growth = Keys('financial-statement-growth', 'growth', "SG&A Expenses Growth")
    operating_expense = Keys('financials/income-statement', 'financials', "Operating Expenses")
    operating_income = Keys('financials/income-statement', 'financials', "Operating Income")

    shortterm_debt = Keys('financials/balance-sheet-statement', 'financials', "Short-term debt")
    total_debt = Keys('financials/balance-sheet-statement', 'financials', "Total debt")
    total_asset = Keys('financials/income-statement', 'financials', "Total assets")
    total_liabilities = Keys('financials/income-statement', 'financials', "Total liabilities")
    pe_ratio = Keys('company-key-metrics', 'financials', "PE ratio")
    pb_ratio = Keys('company-key-metrics', 'financials', "PTB ratio")
    rating = Keys('rating', 'rating', "score")    

if __name__ == "__main__":
    company_data_to_tsdb()