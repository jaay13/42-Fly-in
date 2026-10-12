"""Scheduler tests: booking calendar and room checks."""
from pathlib import Path

from flyin import MapParser
from flyin.scheduler import Scheduler

ROOT = Path(__file__).resolve().parent.parent
FORK = ROOT / "maps" / "easy" / "02_simple_fork.txt"
PRIORITY = ROOT / "maps" / "medium" / "03_priority_puzzle.txt"


def scheduler_for(path: Path) -> Scheduler:
    """Parse a map and return a fresh scheduler for it."""
    return Scheduler(MapParser().parse_file(str(path)))


def test_book_ticks_arrival_zone_and_link() -> None:
    """A one-turn move books the zone at arrival and the link at depart + 1."""
    s = scheduler_for(FORK)
    s._book([("start", 0), ("junction", 1)])
    assert s.zone_use == {("junction", 1): 1}
    assert s.link_use == {(frozenset({"start", "junction"}), 1): 1}


def test_book_wait_uses_no_link() -> None:
    """Waiting books the zone for the next turn but no link."""
    s = scheduler_for(FORK)
    s._book([("start", 0), ("start", 1)])
    assert s.zone_use == {("start", 1): 1}
    assert s.link_use == {}


def test_book_restricted_move_books_link_once() -> None:
    """A two-turn move books the link on the in-flight turn only."""
    s = scheduler_for(PRIORITY)
    s._book([("start", 0), ("slow_path1", 2)])
    assert s.zone_use == {("slow_path1", 2): 1}
    assert s.link_use == {(frozenset({"start", "slow_path1"}), 1): 1}


def test_bookings_add_up_across_routes() -> None:
    """Two drones on the same slot count twice."""
    s = scheduler_for(FORK)
    route = [("start", 0), ("junction", 1)]
    s._book(route)
    s._book(route)
    assert s.zone_use[("junction", 1)] == 2


def test_full_zone_has_no_room() -> None:
    """Junction holds two drones, so a third is refused that turn only."""
    s = scheduler_for(FORK)
    assert s._zone_has_room("junction", 1)
    s._book([("start", 0), ("junction", 1)])
    assert s._zone_has_room("junction", 1)
    s._book([("start", 0), ("junction", 1)])
    assert not s._zone_has_room("junction", 1)
    assert s._zone_has_room("junction", 2)


def test_full_link_has_no_room() -> None:
    """A capacity-one link is refused once booked, from either direction."""
    s = scheduler_for(FORK)
    s._book([("junction", 1), ("path_a", 2)])
    assert not s._link_has_room("junction", "path_a", 2)
    assert not s._link_has_room("path_a", "junction", 2)
    assert s._link_has_room("junction", "path_a", 3)


def test_start_and_end_never_fill_up() -> None:
    """Start and end hubs are unlimited."""
    s = scheduler_for(FORK)
    for _ in range(10):
        s._book([("start", 0), ("start", 1)])
    assert s._zone_has_room("start", 1)


def test_search_finds_earliest_arrival() -> None:
    """On an empty calendar the first drone takes the shortest route."""
    s = scheduler_for(FORK)
    route = s._search()
    assert route[0] == ("start", 0)
    assert route[-1] == ("goal", 3)


def test_search_waits_when_junction_is_full() -> None:
    """With junction full at turn 1, the third drone arrives a turn later."""
    s = scheduler_for(FORK)
    for _ in range(2):
        s._book(s._search())
    route = s._search()
    assert route[1] == ("start", 1)
    assert route[-1] == ("goal", 4)
