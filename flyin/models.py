"""Data classes for the static map: ZoneType, Zone and Connection."""
from dataclasses import dataclass
from enum import Enum


class ZoneType(Enum):
    """The four zone types, using the map file's spelling as the value.

    ``ZoneType("restricted")`` looks a type up by its value and raises
    ValueError for anything that is not one of the four.
    """

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    """One zone (hub) of the map.

    Attributes:
        name: Unique zone name, never containing a dash or space.
        x: Integer x coordinate, only used for drawing.
        y: Integer y coordinate, only used for drawing.
        zone_type: Movement rule for drones entering this zone.
        color: Display colour from the map, or None if not given.
        max_drones: Drones allowed in this zone at the end of a turn.
    """

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1

    @property
    def move_cost(self) -> int:
        """Return the number of turns needed to enter this zone.

        Restricted zones take 2 turns; every other type takes 1.
        """
        return 2 if self.zone_type is ZoneType.RESTRICTED else 1


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
