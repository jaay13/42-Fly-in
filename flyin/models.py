"""Data classes for the static map: ZoneType, Zone and Connection."""
from dataclasses import dataclass
from enum import Enum


class ZoneType(Enum):
    """Zone types, valued by their map file spelling."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    """A zone (hub) of the map."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1

    @property
    def move_cost(self) -> int:
        """Return the turns needed to enter this zone."""
        return 2 if self.zone_type is ZoneType.RESTRICTED else 1


@dataclass
class Connection:
    """A two-way link between two zones."""

    a: str
    b: str
    capacity: int = 1

    @property
    def endpoints(self) -> frozenset[str]:
        """Return both zone names as an order-free key."""
        return frozenset((self.a, self.b))

    @property
    def name(self) -> str:
        """Return the connection name, e.g. ``a-b``."""
        return f"{self.a}-{self.b}"

    def other(self, zone: str) -> str:
        """Return the zone at the opposite end from ``zone``."""
        return self.b if zone == self.a else self.a
