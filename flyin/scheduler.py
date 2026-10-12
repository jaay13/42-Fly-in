"""Plan every drone's route through a shared booking calendar."""

from flyin.graph import Network

Route = list[tuple[str, int]]


class Scheduler:
    """Planner that books zones and links turn by turn."""

    def __init__(self, network: Network) -> None:
        """Start with an empty calendar for the given network."""
        self.network = network
        self.zone_use: dict[tuple[str, int], int] = {}
        self.link_use: dict[tuple[frozenset[str], int], int] = {}

    def plan(self) -> list[Route]:
        """Return one route per drone, in drone order."""
        raise NotImplementedError

    def _search(self) -> Route:
        """Return the earliest-arriving route for the next drone."""
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
