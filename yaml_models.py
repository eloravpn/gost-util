from yamlable import YamlAble, yaml_info


@yaml_info(yaml_tag_ns="com.elora.vpn.gost")
class Auth(YamlAble):
    def __init__(self, username: str, password: str):
        """Constructor"""

        self.username = username
        self.password = password

    def __repr__(self):
        """String representation for prints"""

        return dict(username=self.username, password=self.password)


@yaml_info(yaml_tag_ns="com.elora.vpn.gost")
class Handler(YamlAble):
    def __init__(self, chain: str = None, type_: str = "tcp"):
        """Constructor"""

        self.type = type_
        if chain:
            self.chain = chain


@yaml_info(yaml_tag_ns="com.elora.vpn.gost")
class Listener(YamlAble):
    def __init__(self, auth: Auth = None, backlog: int = 1024, type_: str = "tcp"):
        """Constructor"""

        self.type = type_
        if auth:
            self.auth = auth
        if backlog and type_ == "sshd":
            self.metadata = dict(backlog=backlog)

    # def __repr__(self):
    #     """String representation for prints"""
    #
    #     listener = dict(type=self.type)
    #
    #     if self.chain:
    #         listener["chain"] = self.chain
    #     if self.auth:
    #         listener["auth"] = self.auth
    #     if self.backlog:
    #         listener["metadata"] = dict(backlog=self.backlog)


@yaml_info(yaml_tag_ns="com.elora.vpn.gost")
class Dialer(YamlAble):
    def __init__(self, auth: Auth, type_: str = "sshd"):
        """Constructor"""

        self.auth = auth
        self.type = type_

    def __repr__(self):
        """String representation for prints"""

        return dict(type=self.type, auth=self.auth)


@yaml_info(yaml_tag_ns="com.elora.vpn.gost")
class Connector(YamlAble):
    def __init__(self, type_: str = "sshd"):
        """Constructor"""

        self.type = type_

    def __repr__(self):
        """String representation for prints"""

        return dict(type=self.type)


@yaml_info(yaml_tag_ns="com.elora.vpn.gost")
class Connector(YamlAble):
    def __init__(self, type_: str = "sshd"):
        """Constructor"""

        self.type = type_

    def __repr__(self):
        """String representation for prints"""

        return dict(type=self.type)


@yaml_info(yaml_tag_ns="com.elora.vpn.gost")
class Node(YamlAble):
    def __init__(
        self,
        name: str,
        addr: str,
        connector: Connector = None,
        dialer: Dialer = None,
    ):
        """Constructor"""

        if dialer:
            self.dialer = dialer
        if connector:
            self.connector = connector
        self.addr = addr
        self.name = name

    def __repr__(self):
        """String representation for prints"""

        return dict(
            name=self.name,
            dialer=self.dialer,
            connector=self.connector,
        )
