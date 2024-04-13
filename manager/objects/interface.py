from manager.objects.dhcp_options import DHCPOptions


class Interface:
    def __init__(self, mac_address: str):
        self.interface = f"enx{mac_address}"
        self.dhcp = True
        self.dhcpOptions = DHCPOptions(mac_address)
        self.mtu = 1400
