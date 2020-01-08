from financial_modeling.company_data_to_tsdb import get_company_growth
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

def plot_data(symbol, data: pd.DataFrame, matrix):
    plt.plot(data.index.values, data[matrix], label=matrix)

if __name__ == "__main__":
    data = get_company_growth('aapl')
    for m in ["Asset Growth", "EBIT Growth"]:
        plot_data('aapl', data, m)
    plt.legend(loc="upper left")
    plt.show()