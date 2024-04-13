from manager.objects.cluster import Cluster
from manager.objects.host import HostData
from manager.objects.machine import Machine


class Base:
    def __init__(
        self, base_path: str, name: str, role: str, mac_address: str, host: HostData
    ):
        self.machine = Machine(name, role, mac_address, host)
        self.cluster = Cluster(base_path, name)
