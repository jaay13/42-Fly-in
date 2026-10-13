"""Animated terminal map of the zones and the drones in them."""

import shutil
import sys
import time

from flyin.display import Display
from flyin.graph import Network
from flyin.models import Connection, ZoneType
from flyin.simulation import Simulation

Cell = tuple[str, str]


class MapView:
    """Terminal drawing of the network with drones placed turn by turn."""

    ROW_STEP = 4
    DIM = "\033[38;5;240m"
    FULL = "\033[1;38;5;196m"
    FLIGHT = "\033[1;38;5;226m"
    CLEAR = "\033[2J\033[H"

    def __init__(self, network: Network, simulation: Simulation) -> None:
        """Lay the zones out on a grid that fits the terminal width."""
        self.network = network
        self.simulation = simulation
        self.lines = simulation.lines()
        self.display = Display(network, True)
        self.links: dict[str, Connection] = {
            conn.name: conn for conn in network.connections.values()
        }
        xs = [zone.x for zone in network.zones.values()]
        ys = [zone.y for zone in network.zones.values()]
        self.x0 = min(xs)
        self.y1 = max(ys)
        width = shutil.get_terminal_size((100, 30)).columns
        span = max(xs) - self.x0 + 1
        self.col_step = max(5, min(16, (width - 2) // span))
        self.width = span * self.col_step + 2
        self.height = (self.y1 - min(ys)) * self.ROW_STEP + 3

    def play(self, delay: float = 0.7) -> None:
        """Clear the screen and draw every turn, one after another."""
        for turn in range(len(self.lines) + 1):
            sys.stdout.write(self.CLEAR + self.frame(turn) + "\n")
            sys.stdout.flush()
            time.sleep(delay)

    def frame(self, turn: int) -> str:
        """Return the full picture of the map at ``turn``."""
        where = self.simulation.positions(turn)
        grid: list[list[Cell]] = [
            [(" ", "")] * self.width for _ in range(self.height)
        ]
        for conn in self.network.connections.values():
            self._draw_link(grid, conn)
        for name in self.network.zones:
            self._draw_zone(grid, name, len(where.get(name, [])))
        for spot, drones in where.items():
            if spot in self.links:
                row, col = self._midpoint(self.links[spot])
                self._write(grid, row, col, f"»{len(drones)}", self.FLIGHT)
        body = "\n".join(
            "".join(code + ch + (Display.RESET if code else "")
                    for ch, code in row).rstrip()
            for row in grid
        )
        return self._header(turn, where) + "\n\n" + body + "\n\n" + (
            self._legend())

    def _header(self, turn: int, where: dict[str, list[int]]) -> str:
        """Return the turn counter, the output line and the delivery count."""
        done = len(where.get(self.network.end, []))
        if turn > 0:
            line = self.display.paint(self.lines[turn - 1])
        else:
            line = "(all drones at start)"
        return (f"Turn {turn}/{len(self.lines)}   "
                f"delivered {done}/{self.network.nb_drones}\n{line}")

    def _legend(self) -> str:
        """Return the key to the symbols on the map."""
        return (f"● drone  ○ free place  {self.FULL}●{Display.RESET} full  "
                f"{self.FLIGHT}»n{Display.RESET} n drones in flight  "
                f"✕ blocked")

    def _anchor(self, name: str) -> tuple[int, int]:
        """Return the grid row and column where a zone is drawn."""
        zone = self.network.zones[name]
        return ((self.y1 - zone.y) * self.ROW_STEP + 1,
                (zone.x - self.x0) * self.col_step + 1)

    def _midpoint(self, conn: Connection) -> tuple[int, int]:
        """Return the grid cell halfway along a connection."""
        (r1, c1), (r2, c2) = self._anchor(conn.a), self._anchor(conn.b)
        return (r1 + r2) // 2, (c1 + c2) // 2

    def _draw_link(self, grid: list[list[Cell]], conn: Connection) -> None:
        """Draw a dotted line between the two zones of a connection."""
        (r1, c1), (r2, c2) = self._anchor(conn.a), self._anchor(conn.b)
        steps = max(abs(r2 - r1), abs(c2 - c1), 1)
        for i in range(steps + 1):
            row = round(r1 + (r2 - r1) * i / steps)
            col = round(c1 + (c2 - c1) * i / steps)
            self._write(grid, row, col, "·", self.DIM)

    def _draw_zone(self, grid: list[list[Cell]], name: str,
                   count: int) -> None:
        """Draw a zone's name and its occupancy under it."""
        row, col = self._anchor(name)
        zone = self.network.zones[name]
        colour = self.display.code(zone.color)
        self._write(grid, row, col, name[:self.col_step - 1], colour)
        capacity = self.network.capacity(name)
        if zone.zone_type is ZoneType.BLOCKED:
            self._write(grid, row + 1, col, "✕", self.DIM)
        elif capacity is None:
            self._write(grid, row + 1, col, f"●{count}" if count else "",
                        colour)
        elif count >= capacity:
            self._write(grid, row + 1, col, self._dots(count, capacity),
                        self.FULL)
        else:
            self._write(grid, row + 1, col, self._dots(count, capacity),
                        colour)

    def _dots(self, count: int, capacity: int) -> str:
        """Return filled and free places, or ``n/cap`` if there are many."""
        if capacity > self.col_step - 2:
            return f"{count}/{capacity}"
        return "●" * count + "○" * (capacity - count)

    def _write(self, grid: list[list[Cell]], row: int, col: int,
               text: str, code: str) -> None:
        """Put ``text`` into the grid, clipped at the right edge."""
        for i, ch in enumerate(text):
            if 0 <= row < len(grid) and 0 <= col + i < len(grid[row]):
                grid[row][col + i] = (ch, code)
