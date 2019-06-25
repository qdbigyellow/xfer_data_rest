from typing import List

class Configurations:
    class Server:
        dest : List[str] = ["https://bank.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"]
    
    class DB:
        IP = "192.168.0.6"
        PUSH_GATEWAY = "9091"

