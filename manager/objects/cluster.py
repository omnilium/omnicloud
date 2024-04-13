from manager.objects.inline_manifest import (
    cilium_config_manifest,
    cilium_manifest,
    descheduler_manifest,
    gvisor_manifest,
    kubelet_serving_cert_approver_manifest,
    metrics_server_manifest,
    piraeus_manifest,
)


class Cluster:
    def __init__(self, base_path: str, name: str):
        self.inlineManifests = []

        if name.startswith("master-"):
            self.inlineManifests.append(gvisor_manifest(base_path))
            self.inlineManifests.append(
                kubelet_serving_cert_approver_manifest(base_path)
            )
            self.inlineManifests.append(metrics_server_manifest(base_path))
            self.inlineManifests.append(descheduler_manifest(base_path))
            self.inlineManifests.append(cilium_manifest(base_path))
            self.inlineManifests.append(cilium_config_manifest(base_path))
            self.inlineManifests.append(piraeus_manifest(base_path))
