from manager.objects.interface import Interface


class Network:
    def __init__(self, name: str, mac_address: str):
        self.hostname = f"{name}.omnilium.local"
        self.interfaces = [Interface(mac_address)]
