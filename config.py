from typing import List

class Configurations:
    class Server:
        dest : List[str] = ["https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"]
    
    class DB:
        INFLUXHOST = "localhost"
        INFLUXPORT = "8086"
        DBNAME = "MortageLoan"

