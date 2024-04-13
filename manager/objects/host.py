from enum import Enum


class HostData:
    def __init__(self, name: str, region: str, data_center: str):
        self.name = f"{region}-{name}"
        self.region = region
        self.data_center = f"{region}-{data_center}"


class Host(Enum):
    MASTER_1 = HostData("master-1", "hel1", "dc7")
    STORAGE_1 = HostData("storage-1", "hel1", "dc8")
    WORKER_1 = HostData("worker-1", "hel1", "dc6")
    WORKER_2 = HostData("worker-2", "hel1", "dc8")
    WORKER_3 = HostData("worker-3", "hel1", "dc7")
