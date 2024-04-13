from manager.objects.host import HostData
from manager.objects.network import Network
from manager.objects.role import Role


class Machine:
    def __init__(self, name: str, role: str, mac_address: str, host: HostData):
        self.network = Network(name, mac_address)
        self.nodeLabels = {
            "topology.kubernetes.io/region": host.region,
            "topology.kubernetes.io/zone": host.data_center,
            "topology.omnilium.cloud/host": host.name,
            "node.omnilium.cloud/name": name,
            "node.omnilium.cloud/role": role,
            f"node-role.omnilium.cloud/{role}": "",
            "linstor.omnilium.cloud/deploy": "true",
        }

        if role == Role.CONTROL_PLANE.value:
            self.nodeLabels["node.omnilium.cloud/storage"] = "none"
            self.nodeLabels["linstor.omnilium.cloud/deploy"] = "false"
        elif role == Role.STORAGE.value:
            self.nodeLabels["node.omnilium.cloud/storage"] = "spinning-disk"
        else:
            self.nodeLabels["node.omnilium.cloud/storage"] = "solid-state"
