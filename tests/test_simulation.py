"""Simulation tests: capacity, restricted zones, output format."""
from pathlib import Path

from flyin import MapParser
from flyin.scheduler import Route
from flyin.simulation import Simulation

ROOT = Path(__file__).resolve().parent.parent
FORK = ROOT / "maps" / "easy" / "02_simple_fork.txt"
PRIORITY = ROOT / "maps" / "medium" / "03_priority_puzzle.txt"


def lines_for(path: Path, routes: list[Route]) -> list[str]:
    """Parse a map and print the given routes on it."""
    return Simulation(MapParser().parse_file(str(path)), routes).lines()


def test_normal_moves_print_destination() -> None:
    """Each move prints the zone the drone lands in."""
    route = [("start", 0), ("junction", 1), ("path_a", 2), ("goal", 3)]
    assert lines_for(FORK, [route]) == [
        "D1-junction", "D1-path_a", "D1-goal",
    ]


def test_waits_are_left_out() -> None:
    """A drone that stays put prints nothing that turn."""
    route = [("start", 0), ("start", 1), ("junction", 2)]
    assert lines_for(FORK, [route]) == ["", "D1-junction"]


def test_drones_share_a_line() -> None:
    """Moves in the same turn go on one line, in drone order."""
    a = [("start", 0), ("junction", 1)]
    b = [("start", 0), ("junction", 1)]
    assert lines_for(FORK, [a, b]) == ["D1-junction D2-junction"]


def test_restricted_move_prints_connection_in_flight() -> None:
    """A two-turn move prints the connection, then the zone."""
    route = [("start", 0), ("slow_path1", 2)]
    assert lines_for(PRIORITY, [route]) == [
        "D1-start-slow_path1", "D1-slow_path1",
    ]


def test_positions_track_waits_and_moves() -> None:
    """A waiting drone stays put while a moving one advances."""
    a = [("start", 0), ("junction", 1)]
    b = [("start", 0), ("start", 1), ("junction", 2)]
    sim = Simulation(MapParser().parse_file(str(FORK)), [a, b])
    assert sim.positions(0) == {"start": [1, 2]}
    assert sim.positions(1) == {"junction": [1], "start": [2]}
    assert sim.positions(2) == {"junction": [1, 2]}


def test_positions_show_drone_in_flight() -> None:
    """Mid restricted move, the drone sits on the connection."""
    route = [("start", 0), ("slow_path1", 2)]
    sim = Simulation(MapParser().parse_file(str(PRIORITY)), [route])
    assert sim.positions(1) == {"start-slow_path1": [1]}
    assert sim.positions(2) == {"slow_path1": [1]}


def test_positions_after_the_end_stay_at_goal() -> None:
    """Once its route is over, a drone stays in its last zone."""
    route = [("start", 0), ("junction", 1), ("path_a", 2), ("goal", 3)]
    sim = Simulation(MapParser().parse_file(str(FORK)), [route])
    assert sim.positions(99) == {"goal": [1]}
