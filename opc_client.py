from opcua import Client

ENDPOINT = "opc.tcp://0.0.0.0:4840"
NAMESPACE_URI = "https://data-science.uz/telemetry"  
# --- новый список колонок (кроме DATETIME) ---------------------
CSV_TAGS = [
    "WELLID", "P1", "T1", "P3", "P4", "T4",
    "P7", "T7", "T8", "H1", "T9",
    "V1", "Q1", "Q_G"
]

# --- …

NODE_MAP = {tag: tag for tag in CSV_TAGS}     # имя OPC-узла = имя в JSON

class OPCReader:
    def __init__(self):
        self.client = Client(ENDPOINT)
        self.idx = None
        self.nodes = {}

    def connect(self):
        self.client.connect()
        self.idx = self.client.get_namespace_index(NAMESPACE_URI)
        root = self.client.get_root_node().get_child(["0:Objects", f"{self.idx}:Well"])
        self.nodes = {json_key: root.get_child(f"{self.idx}:{opc_tag}")
                      for opc_tag, json_key in NODE_MAP.items()}
        self.time_node = root.get_child(f"{self.idx}:DATETIME")

    def read_snapshot(self):
        snap = {"timestamp": self.time_node.get_value().isoformat()}
        for k, node in self.nodes.items():
            snap[k] = float(node.get_value())
        return snap
    
    def close(self):
        self.client.disconnect()
