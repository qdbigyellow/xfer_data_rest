from financial_modeling.company_data_to_tsdb import get_company_growth, get_remote_data, Keys, SupportKeys, get_remote_symbol_list
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import click 
from os import path

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
    dest = path.join(path.abspath(__file__), 'all_company_matrix.csv')
    if not path.exists(dest) or update_datasource is True : 
        data_source = get_metrics_all_company(to_csv=True)
    else:
        data_source = pd.read_csv(dest)
    data = data_source[matrix]
    print(data)

def get_metrics_all_company(to_csv=True, index=0):
    symbols = get_remote_symbol_list()
    data_dict = {}
    for s in symbols:
        data_list = []
        key_metrics = get_remote_data(symbol=s, report='company-key-metrics')
        if len(key_metrics) < 1 :
            continue

        growth = get_remote_data(symbol=s, report='financial-statement-growth')
        if len(growth) < 1:
            continue
        
        print(s)
        print(key_metrics[SupportKeys.pb_ratio.path][index][SupportKeys.pb_ratio.value])
        data_list.append(float(key_metrics[SupportKeys.pb_ratio.path][index][SupportKeys.pb_ratio.value]) if key_metrics[SupportKeys.pb_ratio.path][index][SupportKeys.pb_ratio.value] is not "" else 0.0)
        print(key_metrics[SupportKeys.pe_ratio.path][index][SupportKeys.pe_ratio.value])
        data_list.append(float(key_metrics[SupportKeys.pe_ratio.path][index][SupportKeys.pe_ratio.value]) if key_metrics[SupportKeys.pe_ratio.path][index][SupportKeys.pe_ratio.value] is not "" else 0.0)
        print(growth[SupportKeys.ebit_growth.path][index][SupportKeys.ebit_growth.value])
        data_list.append(float(growth[SupportKeys.ebit_growth.path][index][SupportKeys.ebit_growth.value]) if growth[SupportKeys.ebit_growth.path][index][SupportKeys.ebit_growth.value] is not "" else 0.0)
        print(growth[SupportKeys.eps_growth.path][index][SupportKeys.eps_growth.value])
        data_list.append(float(growth[SupportKeys.eps_growth.path][index][SupportKeys.eps_growth.value]) if growth[SupportKeys.eps_growth.path][index][SupportKeys.eps_growth.value] is not "" else 0.0)
        print(growth[SupportKeys.free_cash_flow_growth.path][index][SupportKeys.free_cash_flow_growth.value])
        data_list.append(float(growth[SupportKeys.free_cash_flow_growth.path][index][SupportKeys.free_cash_flow_growth.value]) if growth[SupportKeys.free_cash_flow_growth.path][index][SupportKeys.free_cash_flow_growth.value] is not "" else 0.0)
        data_dict[s] = data_list
    data = pd.DataFrame.from_dict(data_dict, orient='index',columns=['PB Ratio', 'PE Ratio', 'EBIT Growth', 'EPS Growth', 'Cashflow Growth'])
    if to_csv:
        dest = path.join(path.dirname(__file__), 'all_company_matrix.csv')
        data.to_csv(dest)
    return data








#%%


if __name__ == "__main__":
    main()
