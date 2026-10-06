"""Tests for the static map models."""
from flyin.graph import Network
from flyin.models import Connection, Zone


def test_linear_path() -> None:
    """Build easy/01 by hand and check the network wiring."""
    network = Network(2, "start", "goal")

    network.add_zone(Zone("start", 0, 0))
    network.add_zone(Zone("waypoint1", 1, 0))
    network.add_zone(Zone("waypoint2", 2, 0))
    network.add_zone(Zone("goal", 3, 0))

    network.add_connection(Connection("start", "waypoint1"))
    network.add_connection(Connection("waypoint1", "waypoint2"))
    network.add_connection(Connection("waypoint2", "goal"))

    assert network.neighbours["waypoint1"] == ["start", "waypoint2"]
    assert network.link("waypoint2", "waypoint1").name == "waypoint1-waypoint2"
    assert network.capacity("start") is None
    assert network.is_reachable()
