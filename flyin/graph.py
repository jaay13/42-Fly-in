"""Network: the graph of zones and connections."""
from dataclasses import dataclass, field

from .models import Connection, Zone, ZoneType


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
        """Register a zone under its name."""
        self.zones[zone.name] = zone

    def add_connection(self, conn: Connection) -> None:
        """Register a connection and link both zones as neighbours."""
        self.connections[conn.endpoints] = conn
        self.neighbours.setdefault(conn.a, []).append(conn.b)
        self.neighbours.setdefault(conn.b, []).append(conn.a)

    def link(self, u: str, v: str) -> Connection:
        """Return the connection between two adjacent zones."""
        return self.connections[frozenset((u, v))]

    def capacity(self, name: str) -> int | None:
        """Return a zone's capacity, or None if unlimited (start/end)."""
        if name in (self.start, self.end):
            return None
        return self.zones[name].max_drones

    def is_reachable(self) -> bool:
        """Return True if the end can be reached avoiding blocked zones."""
        queue: list[str] = [self.start]
        seen: set[str] = {self.start}

        while queue:
            zone = queue.pop(0)
            if zone == self.end:
                return True
            for neighbor in self.neighbours.get(zone, []):
                if neighbor in seen:
                    continue
                if self.zones[neighbor].zone_type is ZoneType.BLOCKED:
                    continue
                seen.add(neighbor)
                queue.append(neighbor)
        return False
