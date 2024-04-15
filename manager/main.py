# https://click.palletsprojects.com/en/8.1.x/
import click
from manager.objects.base import Base
from manager.objects.cluster import Cluster
from manager.objects.dhcp_options import DHCPOptions
from manager.objects.inline_manifest import InlineManifest
from manager.objects.interface import Interface
from manager.objects.machine import Machine
from manager.objects.network import Network
from ruamel.yaml import YAML
import subprocess
from manager.objects.node import nodes
from manager.objects.role import Role


cluster_name = "omnicloud"
cluster_endpoint = "https://talos.omnilium.local:6443"
base_path = "manifests/talos"
sops_paths = [
    "manifests/cert-manager/omnicloud-ca.yaml",
    "manifests/flagsmith/cnpg-password.yaml",
    "manifests/flagsmith/release.yaml",
    "manifests/forgejo/image-pull-secret.yaml",
    "manifests/forgejo/cnpg-password.yaml",
    "manifests/forgejo/release.yaml",
    "manifests/roundcube/cnpg-password.yaml",
    "manifests/roundcube/release.yaml",
    "manifests/woodpecker/release.yaml",
    f"{base_path}/kustomizations/piraeus/linstor-passphrase.yaml",
    f"{base_path}/secrets.yaml",
    "talosconfig",
]


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
def cli():
    pass


@cli.group(name="talos")
def talos():
    pass


@talos.command("nodes")
def list_nodes():
    for node in nodes[Role.ALL.value]:
        click.echo(node)


@talos.command("generate-secrets")
def generate_secrets():
    subprocess.run(
        [
            "talosctl",
            "gen",
            "secrets",
            "--output-file",
            f"{base_path}/secrets.yaml",
            "--force",
        ]
    )


@talos.command("generate-config")
def generate_config():
    subprocess.run(
        [
            "talosctl",
            "gen",
            "config",
            "--with-secrets",
            f"{base_path}/secrets.yaml",
            "--output-types",
            "talosconfig",
            "--output",
            "talosconfig",
            "--force",
            cluster_name,
            cluster_endpoint,
        ]
    )


@talos.command("generate-base")
@click.option("-n", "--node", "target_nodes", type=click.STRING, multiple=True)
@click.option(
    "-r",
    "--role-filter",
    type=click.Choice(
        [
            Role.ALL.value,
            Role.CONTROL_PLANE.value,
            Role.STORAGE.value,
            Role.WORKER.value,
        ]
    ),
    default=Role.ALL.value,
    show_default=True,
)
def generate_base(target_nodes: list[str], role_filter: str):
    if len(target_nodes) > 0:
        filtered_nodes = [
            node for node in nodes[Role.ALL.value] if node.name in target_nodes
        ]
    else:
        filtered_nodes = nodes[role_filter]

    if not filtered_nodes or len(filtered_nodes) == 0:
        raise click.ClickException(f"Invalid role {role_filter}")

    yaml = YAML()
    yaml.register_class(DHCPOptions)
    yaml.register_class(Interface)
    yaml.register_class(Network)
    yaml.register_class(Machine)
    yaml.register_class(InlineManifest)
    yaml.register_class(Cluster)
    yaml.register_class(Base)

    for node in filtered_nodes:
        with open(f"{base_path}/base/{node.name}.yaml", "w") as file:
            yaml.dump(node.to_base(base_path), file)


@talos.command("render")
@click.option("-n", "--node", "target_nodes", type=click.STRING, multiple=True)
@click.option(
    "-r",
    "--role-filter",
    type=click.Choice(
        [
            Role.ALL.value,
            Role.CONTROL_PLANE.value,
            Role.STORAGE.value,
            Role.WORKER.value,
        ]
    ),
    default=Role.ALL.value,
    show_default=True,
)
def render(target_nodes: list[str], role_filter: str):
    if len(target_nodes) > 0:
        filtered_nodes = [
            node for node in nodes[Role.ALL.value] if node.name in target_nodes
        ]
    else:
        filtered_nodes = nodes[role_filter]

    if not filtered_nodes or len(filtered_nodes) == 0:
        raise click.ClickException(f"Invalid role {role_filter}")

    for node in filtered_nodes:
        command = [
            "talosctl",
            "gen",
            "config",
            "--output",
            f"{base_path}/rendered/{node.name}.yaml",
            "--output-types",
            node.parsed_role,
            "--with-secrets",
            f"{base_path}/secrets.yaml",
            "--config-patch",
            f"@{base_path}/base/{node.name}.yaml",
            "--config-patch",
            f"@{base_path}/cluster.yaml",
            "--config-patch",
            f"@{base_path}/machine.yaml",
            "--force",
            cluster_name,
            cluster_endpoint,
        ]

        subprocess.run(command)


@talos.command("apply")
@click.option("-n", "--node", "target_nodes", type=click.STRING, multiple=True)
@click.option(
    "-r",
    "--role-filter",
    type=click.Choice(
        [
            Role.ALL.value,
            Role.CONTROL_PLANE.value,
            Role.STORAGE.value,
            Role.WORKER.value,
        ]
    ),
    default=Role.ALL.value,
    show_default=True,
)
@click.option("--insecure", is_flag=True, default=False, show_default=True)
def apply(target_nodes: list[str], role_filter: str, insecure: bool):
    if len(target_nodes) > 0:
        filtered_nodes = [
            node for node in nodes[Role.ALL.value] if node.name in target_nodes
        ]
    else:
        filtered_nodes = nodes[role_filter]

    if not filtered_nodes or len(filtered_nodes) == 0:
        raise click.ClickException(f"Invalid role {role_filter}")

    for node in filtered_nodes:
        command = [
            "talosctl",
            "apply-config",
            "-n",
            node.address,
            "--file",
            f"{base_path}/rendered/{node.name}.yaml",
        ]

        if insecure:
            command.append("--insecure")

        subprocess.run(command)


@talos.command("bootstrap")
@click.option(
    "-n",
    "--node",
    "target_node",
    type=click.STRING,
    default="master-1",
    show_default=True,
)
def bootstrap(target_node: str):
    filtered_node = next(
        (node for node in nodes[Role.CONTROL_PLANE.value] if node.name == target_node),
        None,
    )

    if not filtered_node:
        raise click.ClickException(f"Invalid node {target_node}")

    subprocess.run(
        [
            "talosctl",
            "bootstrap",
            "-e",
            filtered_node.address,
            "-n",
            filtered_node.address,
        ]
    )


@talos.command("post-bootstrap")
def post_bootstrap():
    for node in nodes[Role.ALL.value]:
        if len(node.taints) > 0:
            for taint in node.taints:
                subprocess.run(
                    ["kubectl", "taint", "nodes", node.name, f"{taint[0]}={taint[1]}"]
                )

    subprocess.run(
        [
            "flux",
            "install",
            "--namespace=flux-system",
            "--toleration-keys=node-role.kubernetes.io/control-plane",
        ]
    )

    process = subprocess.run(
        [
            "gpg",
            "--export-secret-keys",
            "--armor",
            "0F003E832B1DA1A11CA9F206712F90FA248BBBC2",
        ],
        stdout=subprocess.PIPE,
    )

    subprocess.run(
        [
            "kubectl",
            "create",
            "secret",
            "generic",
            "sops-gpg",
            "--namespace=flux-system",
            "--from-file=sops.asc=/dev/stdin",
        ],
        input=process.stdout,
    )

    subprocess.run(["kubectl", "apply", "-k", "manifests/flux"])


@talos.command("reset")
@click.option("-n", "--node", "target_nodes", type=click.STRING, multiple=True)
@click.option(
    "-r",
    "--role-filter",
    type=click.Choice(
        [
            Role.ALL.value,
            Role.CONTROL_PLANE.value,
            Role.STORAGE.value,
            Role.WORKER.value,
        ]
    ),
    default=Role.ALL.value,
    show_default=True,
)
@click.option("--graceful/--immediate", default=True, show_default=True)
@click.option("--insecure", is_flag=True, default=False, show_default=True)
@click.option("--reboot/--shutdown", default=False, show_default=True)
@click.option("--wait", type=click.BOOL, default=True, show_default=True)
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="This will completely wipe all data and remove the node from the cluster! Are you sure?",
)
def reset(
    target_nodes: list[str],
    role_filter: str,
    graceful: bool,
    insecure: bool,
    reboot: bool,
    wait: bool,
):
    if len(target_nodes) > 0:
        filtered_nodes = [
            node for node in nodes[Role.ALL.value] if node.name in target_nodes
        ]
    else:
        filtered_nodes = nodes[role_filter]

    if not filtered_nodes or len(filtered_nodes) == 0:
        raise click.ClickException(f"Invalid role {role_filter}")

    for node in filtered_nodes:
        command = [
            "talosctl",
            "reset",
            "-e",
            node.address,
            "-n",
            node.address,
            f"--graceful={str(graceful).lower()}",
            f"--wait={str(wait).lower()}",
        ]

        if insecure:
            command.append("--insecure")

        if reboot:
            command.append("--reboot")

        if node.role != Role.CONTROL_PLANE.value:
            command.append("--user-disks-to-wipe")
            command.append("/dev/sdb")

        if node.role == Role.STORAGE.value:
            command.append("--user-disks-to-wipe")
            command.append("/dev/sdc")

        subprocess.call(command)


@cli.group(name="sops")
def sops():
    pass


@sops.command("encrypt")
def encrypt():
    for path in sops_paths:
        subprocess.run(
            ["sops", "-e", "-i", "--input-type", "yaml", "--output-type", "yaml", path]
        )


@sops.command("decrypt")
def decrypt():
    for path in sops_paths:
        subprocess.run(
            ["sops", "-d", "-i", "--input-type", "yaml", "--output-type", "yaml", path]
        )
