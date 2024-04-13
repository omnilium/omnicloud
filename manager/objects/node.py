from manager.objects.base import Base
from manager.objects.host import Host, HostData
from manager.objects.role import Role


class Node:
    def __init__(self, name: str, address: str, mac_address: str, host: HostData):
        self.name = name
        self.address = address
        self.mac_address = mac_address.lower().replace(":", "")
        self.host = host
        self.taints = []

        if name.startswith("master-"):
            self.role = Role.CONTROL_PLANE.value
        elif name.startswith("storage-"):
            self.role = Role.STORAGE.value
            self.taints.append(("storage", "spinning-disk:NoSchedule"))
        else:
            self.role = Role.WORKER.value

    def __str__(self) -> str:
        return f"[{self.role:>13}] {self.name:>9} :: {self.address:<9}"

    @property
    def parsed_role(self):
        if self.role == Role.CONTROL_PLANE.value:
            return "controlplane"
        else:
            return "worker"

    def to_base(self, base_path: str) -> Base:
        return Base(base_path, self.name, self.role, self.mac_address, self.host)


_all = [
    Node("master-1", "10.0.0.3", "BC:24:11:9C:DA:22", Host.MASTER_1.value),
    Node("master-2", "10.0.0.10", "BC:24:11:8B:9A:8F", Host.WORKER_1.value),
    Node("master-3", "10.0.0.11", "BC:24:11:7A:06:20", Host.WORKER_2.value),
    Node("storage-1", "10.0.0.13", "BC:24:11:5A:1E:19", Host.STORAGE_1.value),
    Node("storage-2", "10.0.0.14", "BC:24:11:AB:4E:A2", Host.STORAGE_1.value),
    Node("storage-3", "10.0.0.15", "BC:24:11:65:98:E2", Host.STORAGE_1.value),
    Node("worker-1", "10.0.0.4", "BC:24:11:48:EF:0E", Host.WORKER_1.value),
    Node("worker-2", "10.0.0.5", "BC:24:11:00:C9:4A", Host.WORKER_2.value),
    Node("worker-3", "10.0.0.6", "BC:24:11:EF:89:48", Host.WORKER_3.value),
    Node("worker-4", "10.0.0.7", "BC:24:11:2C:68:A3", Host.WORKER_1.value),
    Node("worker-5", "10.0.0.8", "BC:24:11:25:81:38", Host.WORKER_2.value),
    Node("worker-6", "10.0.0.9", "BC:24:11:51:14:C8", Host.WORKER_3.value),
    Node("worker-7", "10.0.0.18", "BC:24:11:87:6E:80", Host.WORKER_1.value),
    Node("worker-8", "10.0.0.19", "BC:24:11:9E:F9:30", Host.WORKER_2.value),
    Node("worker-9", "10.0.0.20", "BC:24:11:59:1B:A8", Host.WORKER_3.value),
]

nodes = {
    Role.ALL.value: _all,
    Role.CONTROL_PLANE.value: [
        node for node in _all if node.role == Role.CONTROL_PLANE.value
    ],
    Role.STORAGE.value: [node for node in _all if node.role == Role.STORAGE.value],
    Role.WORKER.value: [node for node in _all if node.role == Role.WORKER.value],
}
