"""Find paths from start to end, weighted by zone movement cost."""

from flyin.errors import UnsolvableError
from flyin.graph import Network
from flyin.models import ZoneType


class Pathfinder:
    def __init__(self, network: Network) -> None:
        self.network = network

    def shortest_path(self) -> list[str]:
        start = self.network.start
        goal = self.network.end
        queue: list[str] = [start]
        came_from: dict[str, str | None] = {start: None}

        while queue:
            zone = queue.pop(0)
            if zone == goal:
                return self._build_path(came_from, goal)

            for neighbor in self.network.neighbours.get(zone, []):
                if self.network.zones[neighbor].zone_type is ZoneType.BLOCKED:
                    continue
                if neighbor not in came_from:
                    came_from[neighbor] = zone
                    queue.append(neighbor)
        raise UnsolvableError(f"no path from {start!r} to {goal!r}")

    def _build_path(
        self, came_from: dict[str, str | None], goal: str
    ) -> list[str]:
        path: list[str] = []
        zone: str | None = goal
        while zone is not None:
            path.append(zone)
            zone = came_from[zone]
        return path[::-1]
