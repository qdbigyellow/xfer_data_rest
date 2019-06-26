from typing import List

class Configurations:
    class Server:
        dest : List[str] = ["https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"]
    
    class DB:
        IP = "172.19.0.3"
        PUSH_GATEWAY = "9091"

