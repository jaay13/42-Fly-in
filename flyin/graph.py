"""Graph of zones and connections (adjacency, lookup by name)."""
from dataclasses import dataclass, field

from flyin.models import Connection, Zone


@dataclass
class Network:
    """The whole static map: every zone and connection.

    Attributes:
        nb_drones: Number of drones that start at the start hub.
        start: Name of the start hub.
        end: Name of the end hub.
        zones: Every zone, by name.
        connections: Every connection, by frozenset({a, b}).
        neighbours: Adjacency list: zone name -> neighbouring zone names.
    """

    nb_drones: int
    start: str
    end: str
    zones: dict[str, Zone] = field(default_factory=dict)
    connections: dict[frozenset[str], Connection] = field(
        default_factory=dict)
    neighbours: dict[str, list[str]] = field(default_factory=dict)
