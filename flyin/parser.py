"""Parse and validate a map file into a Network."""
from flyin.graph import Network
from flyin.models import Zone, Connection, ZoneType
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
                    body, _, meta = rest.partition("[")
                    name, x, y = body.split()
                    zone = Zone(name, int(x), int(y))

                    for item in meta.rstrip("]").split():
                        key, _, value = item.partition("=")
                        if key == "zone":
                            zone.zone_type = ZoneType(value)
                        elif key == "color":
                            zone.color = value
                        elif key == "max_drones":
                            zone.max_drones = int(value)
                    zones.append(zone)
                    if prefix == "start_hub":
                        start = name
                    elif prefix == "end_hub":
                        end = name
                elif prefix == "nb_drones":
                    nb_drones = int(rest)
                elif prefix == "connection":
                    body, _, meta = rest.partition("[")
                    a, b = body.strip().split("-")
                    connection = Connection(a, b)
                    for item in meta.rstrip("]").split():
                        _, _, value = item.partition("=")
                        connection.capacity = int(value)
                    connections.append(connection)
                else:
                    raise ParseError(line_nbr, f"{raw_line}")
        network = Network(nb_drones, start, end)
        for zone in zones:
            network.add_zone(zone)
        for connection in connections:
            network.add_connection(connection)
        return network
