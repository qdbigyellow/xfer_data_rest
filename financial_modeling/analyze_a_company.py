from financial_modeling.company_data_to_tsdb import get_company_growth
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




if __name__ == "__main__":
    symbol = 'fds'
    data = get_company_growth(symbol)
    for m in PROFIT_LIST:
        plot_data(symbol, data, m)
#%%
    plt.legend(loc="upper left")
    plt.show()