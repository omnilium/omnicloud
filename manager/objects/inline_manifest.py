import subprocess
from textwrap import dedent
from ruamel.yaml.scalarstring import LiteralScalarString


class InlineManifest:
    def __init__(self, name: str, contents: str):
        self.name = name
        self.contents = LiteralScalarString(dedent(contents))


def gvisor_manifest(base_path: str) -> InlineManifest:
    result = subprocess.run(
        [
            "kubectl",
            "kustomize",
            f"{base_path}/kustomizations/gvisor",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr.decode("utf-8"))

    return InlineManifest("gvisor", result.stdout.decode("utf-8"))


def kubelet_serving_cert_approver_manifest(base_path: str) -> InlineManifest:
    result = subprocess.run(
        [
            "kubectl",
            "kustomize",
            f"{base_path}/kustomizations/kubelet-serving-cert-approver",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr.decode("utf-8"))

    return InlineManifest(
        "kubelet-serving-cert-approver", result.stdout.decode("utf-8")
    )


def metrics_server_manifest(base_path: str) -> InlineManifest:
    result = subprocess.run(
        [
            "kubectl",
            "kustomize",
            f"{base_path}/kustomizations/metrics-server",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr.decode("utf-8"))

    return InlineManifest("metrics-server", result.stdout.decode("utf-8"))


def descheduler_manifest(base_path: str) -> InlineManifest:
    result = subprocess.run(
        [
            "kubectl",
            "kustomize",
            f"{base_path}/kustomizations/descheduler",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr.decode("utf-8"))

    return InlineManifest("descheduler", result.stdout.decode("utf-8"))


def cilium_manifest(base_path: str) -> InlineManifest:
    result = subprocess.run(
        [
            "helm",
            "template",
            "cilium",
            "cilium/cilium",
            "--version",
            "1.16.0-pre.1",
            "--namespace",
            "kube-system",
            "--values",
            f"{base_path}/values/cilium.yaml",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr.decode("utf-8"))

    return InlineManifest("cilium", result.stdout.decode("utf-8"))


def cilium_config_manifest(base_path: str) -> InlineManifest:
    result = subprocess.run(
        [
            "kubectl",
            "kustomize",
            f"{base_path}/kustomizations/cilium",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr.decode("utf-8"))

    return InlineManifest("cilium-config", result.stdout.decode("utf-8"))


def piraeus_manifest(base_path: str) -> InlineManifest:
    result = subprocess.run(
        [
            "kubectl",
            "kustomize",
            f"{base_path}/kustomizations/piraeus",
        ],
        capture_output=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr.decode("utf-8"))

    return InlineManifest("piraeus", result.stdout.decode("utf-8"))
