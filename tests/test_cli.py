"""End-to-end tests of ``fly_in.py``: output, errors and exit status."""
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(*args: str) -> subprocess.CompletedProcess[str]:
    """Run ``fly_in.py`` with the given arguments."""
    return subprocess.run(
        [sys.executable, str(ROOT / "fly_in.py"), *args],
        capture_output=True, text=True, cwd=ROOT,
    )


def test_prints_one_line_per_turn() -> None:
    """A valid map prints only movement lines, exit status 0."""
    result = run("maps/easy/02_simple_fork.txt")
    assert result.returncode == 0
    assert result.stdout.splitlines() == [
        "D1-junction D2-junction",
        "D1-path_a D2-path_b D3-junction D4-junction",
        "D1-goal D2-goal D3-path_a D4-path_b",
        "D3-goal D4-goal",
    ]
    assert result.stderr == ""


def test_unreachable_end_is_an_error() -> None:
    """An unsolvable map reports on stderr and exits with 1."""
    result = run("tests/valid_maps/end_not_connected.txt")
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr.startswith("Error: no path")


def test_missing_file_is_an_error() -> None:
    """A missing file reports on stderr and exits with 1."""
    result = run("does_not_exist.txt")
    assert result.returncode == 1
    assert result.stderr.startswith("Error:")


def test_binary_file_is_an_error() -> None:
    """A file that is not UTF-8 text is reported, not a traceback."""
    result = run("tests/broken_maps/not_utf8.txt")
    assert result.returncode == 1
    assert result.stderr == "Error: line 3: not valid UTF-8 text\n"


def test_wrong_argument_count_prints_usage() -> None:
    """No map argument prints the usage line and exits with 1."""
    result = run()
    assert result.returncode == 1
    assert "usage" in result.stderr


def test_visual_flag_plays_the_map() -> None:
    """``--visual`` draws every turn and exits with 0."""
    result = run("maps/easy/02_simple_fork.txt", "--visual")
    assert result.returncode == 0
    assert "Turn 4/4" in result.stdout
    assert "delivered 4/4" in result.stdout


def test_ctrl_c_stops_visual_without_traceback() -> None:
    """Ctrl-C during ``--visual`` exits with 130 and no traceback."""
    process = subprocess.Popen(
        [sys.executable, str(ROOT / "fly_in.py"),
         "maps/easy/02_simple_fork.txt", "--visual"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        cwd=ROOT,
    )
    time.sleep(1)
    process.send_signal(signal.SIGINT)
    _, stderr = process.communicate(timeout=10)
    assert process.returncode == 130
    assert "Traceback" not in stderr


def test_unknown_flag_prints_usage() -> None:
    """Any other third argument is rejected."""
    result = run("maps/easy/02_simple_fork.txt", "--oops")
    assert result.returncode == 1
    assert "usage" in result.stderr
