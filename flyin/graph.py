"""Network: the graph of zones and connections."""
from dataclasses import dataclass, field

from flyin.models import Connection, Zone


@dataclass
class Network:
    """The static map: zones, connections and adjacency."""

    nb_drones: int
    start: str
    end: str
    zones: dict[str, Zone] = field(default_factory=dict)
    connections: dict[frozenset[str], Connection] = field(
        default_factory=dict)
    neighbours: dict[str, list[str]] = field(default_factory=dict)

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone

    def add_connection(self, conn: Connection) -> None:
        self.connections[conn.endpoints] = conn
        self.neighbours.setdefault(conn.a, []).append(conn.b)
        self.neighbours.setdefault(conn.b, []).append(conn.a)

    def link(self, u: str, v: str) -> Connection:
        return self.connections[frozenset((u, v))]

    def capacity(self, name: str) -> int | None:
        if name in (self.start, self.end):
            return None
        return self.zones[name].max_drones