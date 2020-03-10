from typing import List

class Configurations:
    class Endpoints:
        nordea_kredit : List[str] = ["https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"]
        finanical_modeling : List[str] = ['financials/income-statement', 'financials/balance-sheet-statement', 'financials/cash-flow-statement', 'financial-ratios', 'enterprise-value', 
                                          'company-key-metrics', 'financial-statement-growth', 'company/rating']
        yr_weather: List[str] = ["Denmark/Capital/Hellerup/"]
     
    class DB:
        IP = "http://pushgateway"  # pushgateway
        PUSH_GATEWAY = "9091"

    class DEV_DB:
        IP = "http://192.168.0.6"
        PUSH_GATEWAY = "9091"

    class YR_Bashboard:
        lines = 16
        job_name = "YR_weather"