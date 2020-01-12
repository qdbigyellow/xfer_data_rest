from financial_modeling.company_data_to_tsdb import get_company_growth, get_remote_data, Keys, SupportKeys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import click 

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

#%%

if __name__ == "__main__":
    main()
