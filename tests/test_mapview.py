"""MapView tests: every frame renders and shows the zone states."""
import re
from pathlib import Path

import pytest

from flyin import MapParser, MapView, Scheduler, Simulation

ROOT = Path(__file__).resolve().parent.parent
SUBJECT_MAPS = sorted((ROOT / "maps").glob("*/*.txt"))
ANSI = re.compile(r"\033\[[0-9;]*[A-Za-z]")


def view_for(path: Path) -> MapView:
    """Plan a map and return its terminal view."""
    network = MapParser().parse_file(str(path))
    return MapView(network, Simulation(network, Scheduler(network).plan()))


@pytest.mark.parametrize("path", SUBJECT_MAPS, ids=lambda p: p.stem)
def test_every_frame_renders(path: Path) -> None:
    """Each turn of each subject map draws without error."""
    view = view_for(path)
    for turn in range(len(view.lines) + 1):
        assert view.frame(turn).startswith(f"Turn {turn}/")


def test_full_zone_and_flight_are_shown() -> None:
    """Junction shows two taken places; a restricted move shows ``»``."""
    fork = view_for(ROOT / "maps" / "easy" / "02_simple_fork.txt")
    assert "●●" in ANSI.sub("", fork.frame(1))
    puzzle = view_for(ROOT / "maps" / "medium" / "03_priority_puzzle.txt")
    assert "»1" in ANSI.sub("", puzzle.frame(1))
