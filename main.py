import ast
import csv
import json
from collections import defaultdict

import yaml

from yaml_models import Handler, Listener, Dialer, Auth, Node, Connector

user_name = "gost"
password = "gost"
connection_limit = 1000
back_log = 8192
limit = "2MB"
request_limit = "5"


def generate_client_config(gost_config_file_name: str = "gost-config.csv"):
    gost_config_file_name = "gost-config.csv"

    file = open(gost_config_file_name, encoding="utf8")
    csvreader = csv.reader(file)

    services = []
    chains = []
    climiters = []
    limiters = []
    rlimiters = []

    for index, row in enumerate(csvreader):
        in_port = row[0]
        ip = row[1]

        start_port = int(row[2])
        end_port = int(row[3])
        step = int(row[4])

        password = row[5]

        nodes = []

        services.append(
            {
                "name": f"service-{in_port}-to-{ip}",
                "climiter": "climiter-0",
                # "limiter": "limiter-0",
                # "rlimiter": "rlimiter-0",
                "addr": f":{in_port}",
                "handler": Handler(chain=f"chain-{in_port}", type_="tcp"),
                "listener": Listener(type_="tcp"),
            }
        )

        for i in range(start_port, end_port + 1, step):
            nodes.append(
                Node(
                    name=f"node-{i}",
                    addr=f"{ip}:{i}",
                    connector=Connector(type_="sshd"),
                    dialer=Dialer(
                        auth=Auth(username=user_name, password=password),
                        type_="sshd",
                        keepalive=True,
                    ),
                )
            )

        chains.append(
            {
                "name": f"chain-{in_port}",
                "hops": [
                    {
                        "name": f"hope-1",
                        "selector": dict(
                            strategy="round", maxFails=3, failTimeout="60s"
                        ),
                        "nodes": nodes,
                    }
                ],
            }
        )

    climiters.append(
        {
            "name": "climiter-0",
            "limits": [f"$$ {connection_limit}"],
        }
    )

    # limiters.append(
    #     {
    #         "name": "limiter-0",
    #         "limits": [f"$$ {limit}"],
    #     }
    # )
    #
    # rlimiters.append(
    #     {
    #         "name": "rlimiter-0",
    #         "limits": [f"$$ {request_limit}"],
    #     }
    # )

    gost = {
        "services": services,
        "chains": chains,
        "climiters": climiters,
        # "limiters": limiters,
        # "rlimiters": rlimiters,
    }

    with open("configs/gost-client.yaml", "w", encoding="utf-8") as f:
        f.write(yaml.dump(gost, sort_keys=False, default_flow_style=False))


def generate_server_config(
    csv_file,
    user_name: str = "gost",
    yaml_file_name: str = "gost-server.yaml",
):
    csvreader = csv.reader(csv_file)

    services = []
    chains = []

    server_config_files = defaultdict(lambda: [])

    for index, row in enumerate(csvreader):
        in_port = row[0]
        ip = row[1]

        start_port = int(row[2])
        end_port = int(row[3])
        step = int(row[4])

        password = row[5]
        xui_port = row[6]
        for i in range(start_port, end_port + 1, step):
            # if not server_config_files[ip]:
            #     server_config_files[ip] = []

            server_config_files[ip].append(
                {
                    "name": f"service-{i}",
                    # "climiter": "climiter-0",
                    # "limiter": "limiter-0",
                    # "rlimiter": "rlimiter-0",
                    "addr": f":{i}",
                    "handler": Handler(type_="forward"),
                    "listener": Listener(
                        type_="sshd",
                        auth=Auth(username=user_name, password=password),
                        backlog=back_log,
                    ),
                    "forwarder": dict(
                        nodes=[
                            Node(name=f"node-{xui_port}", addr=f"127.0.0.1:{xui_port}")
                        ]
                    ),
                }
            )
    print("Keys:", list(server_config_files.keys()))

    for key, value in server_config_files.items():
        gost = {"services": value}

        with open(f"configs/gost-server-{key}.yaml", "w", encoding="utf-8") as f:
            f.write(yaml.dump(gost, sort_keys=False, default_flow_style=False))


if __name__ == "__main__":
    generate_server_config(csv_file=open("gost-config.csv", encoding="utf8"))
    generate_client_config()

    print("Generated!")
