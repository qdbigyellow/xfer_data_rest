from dataclasses import dataclass

@dataclass
class CompanyFigures:
    name: str
    date: str = '1970-01-01'
    gross_profit_growth: float = 0.0
    ebit_growth: float = 0.0
    operating_income_growth: float = 0.0
    net_income_growth: float = 0.0
    eps_growth: float = 0.0
    eps_diluted_growth: float = 0.0
    weighted_average_shares_growth: float = 0.0
    weighted_average_shares_diluted_growth: float = 0.0
    divident_per_share_growth: float = 0.0
    operating_cash_flow_growth: float = 0.0
    free_cash_flow_growth: float = 0.0
    receivables_growth: float = 0.0
    inventory_growth: float = 0.0
    asset_growth: float = 0.0
    book_value_per_share_growth: float = 0.0
    debt_growth: float = 0.0
    rd_expense_growth: float = 0.0
    sga_expense_growth: float = 0.0
    revenue_growth: float = 0.0

    ops_expense_growth: float = 0.0
    ops_expense_to_income_ratio: float = 0.0

    short_term_debt_to_total_ratio: float = 0.0
    asset_to_liability_ratio: float = 0.0

    pe_ratio: float = 0.0
    pb_ratio: float = 0.0
    roe: float = 0.0

    rating: float = 0.0