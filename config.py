from typing import List

class Configurations:
    class Endpoints:
        nordea_kredit : List[str] = ["https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"]
        finanical_modeling : List[str] = ['financials/income-statement', 'financials/balance-sheet-statement', 'financials/cash-flow-statement', 'financial-ratios', 'enterprise-value', 
                                          'company-key-metrics', 'financial-statement-growth', 'company/rating']
     
    class DB:
        IP = "172.19.0.3"
        PUSH_GATEWAY = "9091"

    class DEV_DB:
        IP = "192.168.0.6"
        PUSH_GATEWAY = "9091"

