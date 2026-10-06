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
