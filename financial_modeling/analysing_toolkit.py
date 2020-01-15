from financial_modeling.company_data_to_tsdb import get_company_growth, get_remote_data, Keys, SupportKeys, get_remote_symbol_list
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import click 
from os import path
import asyncio
import time
import aiohttp
import psycopg2

PROFIT_LIST = [
    'Gross Profit Growth',
    'EBIT Growth',
    'Net Income Growth',
    'R&D Expense Growth',
    'SG&A Expenses Growth',
    'Asset Growth',
    'Debt Growth'
]

SHARE_VALUE_LIST = [
    'EPS Growth',
    'Divendend Growth',
    'Book Value per share Growth'
]

CASHFLOW_LIST = [
    'Operation Cashflow Growth',
    'Free Cash Flow Growth',
    'Receivable Growth',
    'Inventory Growth'
]


def plot_data(symbol, data: pd.DataFrame, matrix):
    plt.plot(data.index.values, data[matrix], label=matrix)


def plot_datas(symbol, matrices):
    data = get_company_growth(symbol)
    for m in matrices:
        plot_data(symbol, data, m)
    plt.legend(loc="upper left")
    plt.show()

def get_data(symbol, matrix: Keys):
    matrix_data = []
    data = get_remote_data(symbol=symbol, report=matrix.report)
    for d in data[matrix.path]:
        matrix_data.append(float(d[matrix.value]))
    return matrix_data


def cross_companies_compare(symbols, matrix):
    for s in symbols:
        d = get_data(s, matrix)
        plt.plot(d, label=s)        
    plt.legend(loc="upper left")
    plt.title(f'Compare {matrix.value}')
    plt.show()
    
        
@click.group(context_settings={'help_option_names': ['-h', '--help']},
             help='Analysis the company financial figures')
def main():
    pass

@main.command(name='plot', help="plot the matrix on screen")
@click.option('-s', '--symbols', type=str, help="The symbol of compaines to anaylisis", multiple=True)
@click.option('-m', '--matrices', type=str, help="the matrices to plot. If more than one symbol is provided, maxmimun 1 matrix could be plot", multiple=True)
def plot(symbols, matrices):
    # as multiple=True, input is a SET type
    if len(symbols) > 1:
        if len(matrices) > 1:
            quit()
        cross_companies_compare(symbol, matrics)
    else:
        plot_datas(symbols[0], list(matrices))


available_matrix = [SupportKeys.pb_ratio, SupportKeys.pe_ratio, SupportKeys.ebit_growth, SupportKeys.eps_growth, SupportKeys.free_cash_flow_growth]

@main.command(name='find')
@click.option('-m', '--matrix', type=str, help="Matrix name", required=True)
@click.option('-u', '--update-datasource', type=bool, help="Update the datasource file", default=False,  required=False)
def find(matrix, update_datasource=False, number=20, sort='desc'):
    #TODO: Get data from database, and sort in database instead here. 
    print(data)


@main.command('dbextract')
def dbextract():
    sites = get_remote_symbol_list()
    start_time = time.time()
    a = asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")


async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in sites:
            task = asyncio.ensure_future(download_site(session, symbol))
            tasks.append(task)
        return await asyncio.gather(*tasks, return_exceptions=True)

async def download_site(session, symbol, index=0):
    print(symbol)
    url = f'https://financialmodelingprep.com/api/v3/company-key-metrics/{symbol}?period=quarter'
    async with session.get(url) as response:
        key_metrics = await response.json()

    url = f'https://financialmodelingprep.com/api/v3/financial-statement-growth/{symbol}?period=quarter'
    async with session.get(url) as response:
        growth = await response.json()    

    pb_ratio = 0.0
    pe_ratio = 0.0
    if len(key_metrics) > 0:
        pb_ratio = float(key_metrics[SupportKeys.pb_ratio.path][index][SupportKeys.pb_ratio.value]) if key_metrics[SupportKeys.pb_ratio.path][index][SupportKeys.pb_ratio.value] is not "" else 0.0
        pe_ratio = float(key_metrics[SupportKeys.pe_ratio.path][index][SupportKeys.pe_ratio.value]) if key_metrics[SupportKeys.pe_ratio.path][index][SupportKeys.pe_ratio.value] is not "" else 0.0
    eps_growth = 0.0    
    ebit_growth = 0.0    
    fcf_growth = 0.0    
    if len(growth) > 0:
        ebit_growth = float(growth[SupportKeys.ebit_growth.path][index][SupportKeys.ebit_growth.value]) if growth[SupportKeys.ebit_growth.path][index][SupportKeys.ebit_growth.value] is not "" else 0.0
        eps_growth = float(growth[SupportKeys.eps_growth.path][index][SupportKeys.eps_growth.value]) if growth[SupportKeys.eps_growth.path][index][SupportKeys.eps_growth.value] is not "" else 0.0
        fcf_growth = float(growth[SupportKeys.free_cash_flow_growth.path][index][SupportKeys.free_cash_flow_growth.value]) if growth[SupportKeys.free_cash_flow_growth.path][index][SupportKeys.free_cash_flow_growth.value] is not "" else 0.0

    connection = psycopg2.connect(user = "autouser",
                            password = "autouser",
                            host = "192.168.0.6",
                            port = "5432",
                            database = "homeauto")
    cursor = connection.cursor()

    pg_insert_query = """INSERT INTO public.financial_matrix ("symbol", "EPS_Growth", "FCF_Growth", "PB_Ratio", "PE_Ratio", "EBIT_Growth") VALUES (%s,%s,%s,%s,%s,%s)
       ON CONFLICT ("symbol")
       DO
          UPDATE 
          SET "EPS_Growth" = EXCLUDED."EPS_Growth",
          "FCF_Growth" = EXCLUDED."FCF_Growth",
          "PB_Ratio" = EXCLUDED."PB_Ratio",
          "PE_Ratio" = EXCLUDED."PE_Ratio",
          "EBIT_Growth" = EXCLUDED."EBIT_Growth";
    """
    record_to_insert = (symbol, eps_growth, fcf_growth, pb_ratio, pe_ratio, ebit_growth)
    cursor.execute(pg_insert_query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()

#%%


if __name__ == "__main__":
    main()