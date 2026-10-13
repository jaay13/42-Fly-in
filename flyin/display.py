"""Coloured terminal output of each turn and zone state."""

from flyin.graph import Network


class Display:
    """Painter that colours each move with its destination zone's colour."""

    CODES: dict[str, int] = {
        "black": 244,
        "red": 196,
        "darkred": 88,
        "maroon": 124,
        "crimson": 161,
        "orange": 208,
        "gold": 220,
        "yellow": 226,
        "lime": 118,
        "green": 34,
        "cyan": 51,
        "blue": 33,
        "purple": 129,
        "violet": 177,
        "magenta": 201,
        "brown": 130,
        "gray": 245,
        "grey": 245,
        "white": 255,
        "pink": 218,
    }
    RESET = "\033[0m"

    def __init__(self, network: Network, enabled: bool) -> None:
        """Paint with the network's zone colours when ``enabled``."""
        self.network = network
        self.enabled = enabled

    def _start(self, color: str | None) -> str | None:
        """Return the escape code for ``color``, or None if it is unknown."""
        if color is None or color.lower() not in self.CODES:
            return None
        return f"\033[38;5;{self.CODES[color.lower()]}m"

    def paint(self, line: str) -> str:
        """Return ``line`` with every move coloured like its zone."""
        if not self.enabled:
            return line
        painted: list[str] = []
        for move in line.split():
            zone = move.split("-")[-1]
            start = self._start(self.network.zones[zone].color)
            if start is None:
                painted.append(move)
            else:
                painted.append(start + move + self.RESET)
        return " ".join(painted)
