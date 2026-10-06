"""Parser tests: valid maps and every error case."""
from pathlib import Path

import pytest

from flyin.errors import ParseError
from flyin.parser import MapParser

ROOT = Path(__file__).resolve().parent.parent
SUBJECT_MAPS = sorted((ROOT / "maps").glob("*/*.txt"))
VALID_MAPS = Path(__file__).parent / "valid_maps"
BROKEN_MAPS = Path(__file__).parent / "broken_maps"


@pytest.mark.parametrize("path", SUBJECT_MAPS, ids=lambda p: p.stem)
def test_subject_maps_parse(path: Path) -> None:
    """Every map shipped with the subject loads without errors."""
    network = MapParser().parse_file(str(path))
    assert network.start in network.zones
    assert network.end in network.zones


def test_inline_comments_are_ignored() -> None:
    """Text after # is dropped, wherever it appears on a line."""
    network = MapParser().parse_file(str(VALID_MAPS / "inline_comments.txt"))
    assert (network.nb_drones, network.start, network.end) == (2, "s", "e")
    assert network.neighbours == {"s": ["e"], "e": ["s"]}


@pytest.mark.parametrize("name, line_nb, reason", [
    ("nb_drones_zero", 1, "nb_drones must be positive, got 0"),
    ("nb_drones_negative", 1, "nb_drones must be positive, got -4"),
    ("nb_drones_not_int", 1, "nb_drones must be an integer"),
    ("nb_drones_float", 1, "nb_drones must be an integer"),
    ("nb_drones_not_first", 2, "first line must be 'nb_drones"),
    ("nb_drones_twice", 2, "nb_drones defined twice"),
    ("nb_drones_missing", 1, "file has no nb_drones line"),
    ("empty_file", 1, "file has no nb_drones line"),
])
def test_broken_map(name: str, line_nb: int, reason: str) -> None:
    """Each broken map raises a ParseError naming the line and cause."""
    with pytest.raises(ParseError) as error:
        MapParser().parse_file(str(BROKEN_MAPS / f"{name}.txt"))
    assert error.value.line_nb == line_nb
    assert reason in str(error.value)
