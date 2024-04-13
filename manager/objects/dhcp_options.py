class DHCPOptions:
    def __init__(self, mac_address: str):
        self.ipv6 = True
        self.duidv6 = f"000100012da79d15{mac_address}"
