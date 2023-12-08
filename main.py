import csv

import yaml

from yaml_models import Handler, Listener, Dialer, Auth, Node, Connector

if __name__ == "__main__":
    gost_config_file_name = "gost-config.csv"

    user_name = "gost"
    password = "gost"
    connection_limit = 100
    limit = "2MB"
    request_limit = "5"

    rows = []
    file = open(gost_config_file_name, encoding="utf8")
    csvreader = csv.reader(file)

    services = []
    chains = []
    climiters = []
    limiters = []
    rlimiters = []

    for index, row in enumerate(csvreader):
        password = row[3]
        services.append(
            {
                "name": f"service-{index+1}",
                "climiter": "climiter-0",
                "limiter": "limiter-0",
                "rlimiter": "rlimiter-0",
                "addr": f":{row[0]}",
                "handler": Handler(chain=f"chain-{index+1}", type_="tcp"),
                "listener": Listener(type_="tcp"),
            }
        )

        nodes = [
            Node(
                name=f"node-1",
                addr=f"{row[1]}:{row[2]}",
                connector=Connector(type_="sshd"),
                dialer=Dialer(
                    auth=Auth(username=user_name, password=password), type_="sshd"
                ),
            )
        ]

        chains.append(
            {
                "name": f"chain-{index+1}",
                "hops": [{"name": f"hope-1", "nodes": nodes}],
            }
        )

    climiters.append(
        {
            "name": "climiter-0",
            "limits": [f"$$ {connection_limit}"],
        }
    )

    limiters.append(
        {
            "name": "limiter-0",
            "limits": [f"$$ {limit}"],
        }
    )

    rlimiters.append(
        {
            "name": "rlimiter-0",
            "limits": [f"$$ {request_limit}"],
        }
    )

    gost = {
        "services": services,
        "chains": chains,
        "climiters": climiters,
        "limiters": limiters,
        "rlimiters": rlimiters,
    }

    with open("gost.yaml", "w", encoding="utf-8") as f:
        f.write(yaml.dump(gost, sort_keys=False, default_flow_style=False))

    print("gost.yaml Generated!")
