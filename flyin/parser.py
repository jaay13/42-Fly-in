"""Parse and validate a map file into a Network."""
from flyin.graph import Network
from flyin.models import Zone, Connection
from flyin.errors import ParseError


class MapParser:
    """Reader for the Fly-in map file format."""

    def parse_file(self, path: str) -> Network:
        """Read the map at ``path`` and return its Network."""
        nb_drones = 0
        start = ""
        end = ""
        zones: list[Zone] = []
        connections: list[Connection] = []
        with open(path) as file:
            for line_nbr, line in enumerate(file, start=1):
                raw_line = line.rstrip("\n")
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                prefix, _, rest = line.partition(":")
                if prefix in ("start_hub", "end_hub", "hub"):
                    body = rest.partition("[")[0]
                    name, x, y = body.split()
                    zones.append(Zone(name, int(x), int(y)))
                    if prefix == "start_hub":
                        start = name
                    elif prefix == "end_hub":
                        end = name
                elif prefix == "nb_drones":
                    nb_drones = int(rest)
                elif prefix == "connection":
                    body = rest.partition("[")[0]
                    a, b = body.strip().split("-")
                    connections.append(Connection(a, b))
                else:
                    raise ParseError(line_nbr, f"{raw_line}")
        network = Network(nb_drones, start, end)
        for zone in zones:
            network.add_zone(zone)
        for connection in connections:
            network.add_connection(connection)
        return network
