"""Plan every drone's route through a shared booking calendar."""

import heapq

from flyin.graph import Network
from flyin.models import ZoneType
from flyin.pathfinder import Pathfinder

State = tuple[str, int]
Route = list[State]


class Scheduler:
    """Planner that books zones and links turn by turn."""

    def __init__(self, network: Network) -> None:
        """Start with an empty calendar for the given network."""
        self.network = network
        self.zone_use: dict[tuple[str, int], int] = {}
        self.link_use: dict[tuple[frozenset[str], int], int] = {}

    def plan(self) -> list[Route]:
        """Return one route per drone, in drone order."""
        Pathfinder(self.network).shortest_path()
        routes: list[Route] = []
        for _ in range(self.network.nb_drones):
            route = self._search()
            self._book(route)
            routes.append(route)
        return routes

    def _build_route(
        self, came_from: dict[State, State | None], goal: State
    ) -> Route:
        """Walk ``came_from`` back from ``goal`` and return the route."""
        path: Route = []
        zone: State | None = goal
        while zone is not None:
            path.append(zone)
            zone = came_from[zone]
        return path[::-1]

    def _search(self) -> Route:
        """Return the earliest route, avoiding non-priority zones on ties."""
        start: State = (self.network.start, 0)
        queue: list[tuple[int, int, str]] = [(0, 0, self.network.start)]
        came_from: dict[State, State | None] = {start: None}
        normal_steps: dict[State, int] = {start: 0}
        while queue:
            turn, steps, zone = heapq.heappop(queue)
            if steps > normal_steps[(zone, turn)]:
                continue
            if zone == self.network.end:
                return self._build_route(came_from, (zone, turn))

            moves = [(zone, turn + 1)]
            for neighbor in self.network.neighbours.get(zone, []):
                if self.network.zones[neighbor].zone_type is ZoneType.BLOCKED:
                    continue
                cost = self.network.zones[neighbor].move_cost
                moves.append((neighbor, turn + cost))
            for state in moves:
                nxt, nxt_turn = state
                nxt_steps = steps
                if nxt != zone and (
                    self.network.zones[nxt].zone_type is not ZoneType.PRIORITY
                ):
                    nxt_steps += 1
                if normal_steps.get(state, nxt_steps + 1) <= nxt_steps:
                    continue
                if not self._zone_has_room(nxt, nxt_turn):
                    continue
                if nxt != zone and not self._link_has_room(
                    zone, nxt, turn + 1
                ):
                    continue
                came_from[state] = (zone, turn)
                normal_steps[state] = nxt_steps
                heapq.heappush(queue, (nxt_turn, nxt_steps, nxt))
        raise NotImplementedError

    def _zone_has_room(self, zone: str, turn: int) -> bool:
        """Return True if ``zone`` can take one more drone at ``turn``."""
        capacity = self.network.capacity(zone)
        if capacity is None:
            return True
        key = (zone, turn)
        return capacity > self.zone_use.get(key, 0)

    def _link_has_room(self, a: str, b: str, turn: int) -> bool:
        """Return True if one more drone can start crossing ``a-b``."""
        conn = self.network.link(a, b)
        key = (conn.endpoints, turn)
        return conn.capacity > self.link_use.get(key, 0)

    def _book(self, route: Route) -> None:
        """Reserve every zone and link slot the route uses."""
        for (src, depart), (dst, arrive) in zip(route, route[1:]):
            zone_key = (dst, arrive)
            self.zone_use[zone_key] = self.zone_use.get(zone_key, 0) + 1

            if src != dst:
                link_key = (self.network.link(src, dst).endpoints, depart + 1)
                self.link_use[link_key] = self.link_use.get(link_key, 0) + 1
