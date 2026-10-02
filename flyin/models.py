"""Data classes: Zone, ZoneType, Connection, Drone."""
from dataclasses import dataclass
from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone():
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1


@dataclass
class Connection:
    """A two-way link between two zones, stored by zone name.

    Attributes:
        a: First zone name, as written in the map.
        b: Second zone name, as written in the map.
        capacity: Drones allowed to start crossing it in one turn.
    """

    a: str
    b: str
    capacity: int = 1
