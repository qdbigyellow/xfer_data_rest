from financial_modeling.company_data_to_tsdb import get_company_growth, get_remote_data, Keys, SupportKeys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


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


def plot_datas(symbol):
    data = get_company_growth(symbol)
    for m in PROFIT_LIST:
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
    
        

#%%

if __name__ == "__main__":
    symbols = ['aapl', 'msft']
    cross_companies_compare(symbols, SupportKeys.eps_growth)

