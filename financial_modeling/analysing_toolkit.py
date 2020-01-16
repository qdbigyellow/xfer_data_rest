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
from lib.pg_connector import conn, insert_query

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
    plt.plot(data.index[::-1].values, data[matrix][::-1], label=matrix)


def plot_datas(symbol, metrics):
    data = get_company_growth(symbol)
    for m in metrics:
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
@click.option('-m', '--metrics', type=str, help="the metrics to plot. If more than one symbol is provided, maxmimun 1 matrix could be plot", multiple=True)
def plot(symbols, metrics):
    # as multiple=True, input is a SET type
    if len(symbols) > 1:
        if len(metrics) > 1:
            quit()
        cross_companies_compare(symbols, metrics)
    else:
        plot_datas(symbols[0], list(metrics))


@main.command('dbextract')
def dbextract():
    """Read the give matrix from all available symbols and put the data into postgresql database.  So Grafana can query the database directly from there.
    """
    symbols = get_remote_symbol_list()
    start_time = time.time()
    # a = asyncio.get_event_loop().run_until_complete(download_all_symbols(symbols))
    asyncio.run(download_all_symbols(symbols))
    duration = time.time() - start_time
    print(f"Downloaded {len(symbols)} symbols in {duration} seconds")


async def download_all_symbols(symbols):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in symbols:
            # task = asyncio.ensure_future(download_financial_data(session, symbol))
            task = asyncio.create_task(download_financial_data(session, symbol))
            tasks.append(task)
        # Note use * before tasks to unpack.
        await asyncio.gather(*tasks, return_exceptions=True)

async def download_financial_data(session, symbol, index=0):
    url = f'https://financialmodelingprep.com/api/v3/company-key-metrics/{symbol}?period=quarter'
    async with session.get(url) as response:
        key_metrics = await response.json()

    url = f'https://financialmodelingprep.com/api/v3/financial-statement-growth/{symbol}?period=quarter'
    async with session.get(url) as response:
        growth = await response.json()    

    pb_ratio, pe_ratio, eps_growth, ebit_growth, fcf_growth = read_data(key_metrics, growth)

    connection = conn()
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
    insert_query(connection=connection, query=pg_insert_query, data=record_to_insert)
    connection.close()


def read_data(key_metrics, growth, index=0):
    pb_ratio = 0.0
    pe_ratio = 0.0
    eps_growth = 0.0   
    ebit_growth = 0.0    
    fcf_growth = 0.0    
    if len(key_metrics) > 0:
        pb_ratio = float(key_metrics[SupportKeys.pb_ratio.path][index][SupportKeys.pb_ratio.value]) if key_metrics[SupportKeys.pb_ratio.path][index][SupportKeys.pb_ratio.value] is not "" else 0.0
        pe_ratio = float(key_metrics[SupportKeys.pe_ratio.path][index][SupportKeys.pe_ratio.value]) if key_metrics[SupportKeys.pe_ratio.path][index][SupportKeys.pe_ratio.value] is not "" else 0.0
    if len(growth) > 0:
        ebit_growth = float(growth[SupportKeys.ebit_growth.path][index][SupportKeys.ebit_growth.value]) if growth[SupportKeys.ebit_growth.path][index][SupportKeys.ebit_growth.value] is not "" else 0.0
        eps_growth = float(growth[SupportKeys.eps_growth.path][index][SupportKeys.eps_growth.value]) if growth[SupportKeys.eps_growth.path][index][SupportKeys.eps_growth.value] is not "" else 0.0
        fcf_growth = float(growth[SupportKeys.free_cash_flow_growth.path][index][SupportKeys.free_cash_flow_growth.value]) if growth[SupportKeys.free_cash_flow_growth.path][index][SupportKeys.free_cash_flow_growth.value] is not "" else 0.0
    return pb_ratio, pe_ratio, eps_growth, ebit_growth, fcf_growth

#%%


if __name__ == "__main__":
    main()