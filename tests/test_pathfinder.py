"""Pathfinder tests: shortest routes, blocked zones, unsolvable maps."""
from pathlib import Path

import pytest

from flyin import MapParser, UnsolvableError, ZoneType
from flyin.pathfinder import Pathfinder

ROOT = Path(__file__).resolve().parent.parent
SUBJECT_MAPS = sorted((ROOT / "maps").glob("*/*.txt"))
VALID_MAPS = Path(__file__).parent / "valid_maps"


def route_for(path: Path) -> list[str]:
    """Parse a map and return its shortest route."""
    return Pathfinder(MapParser().parse_file(str(path))).shortest_path()


@pytest.mark.parametrize("path", SUBJECT_MAPS, ids=lambda p: p.stem)
def test_subject_routes_are_valid(path: Path) -> None:
    """Each route runs start to end over real links, never through a wall."""
    network = MapParser().parse_file(str(path))
    route = Pathfinder(network).shortest_path()
    assert route[0] == network.start
    assert route[-1] == network.end
    for here, there in zip(route, route[1:]):
        assert there in network.neighbours[here]
    for zone in route:
        assert network.zones[zone].zone_type is not ZoneType.BLOCKED


def test_linear_route() -> None:
    """A straight line gives every zone in order."""
    route = route_for(ROOT / "maps/easy/01_linear_path.txt")
    assert route == ["start", "waypoint1", "waypoint2", "goal"]


def test_blocked_zone_forces_detour() -> None:
    """A blocked shortcut is skipped for the longer open route."""
    route = route_for(VALID_MAPS / "blocked_detour.txt")
    assert route == ["s", "detour1", "detour2", "e"]


@pytest.mark.parametrize("name", ["blocked_only_route", "end_not_connected"])
def test_unreachable_end_raises(name: str) -> None:
    """No open route to the end raises UnsolvableError naming both hubs."""
    with pytest.raises(UnsolvableError, match="no path from 's' to 'e'"):
        route_for(VALID_MAPS / f"{name}.txt")
