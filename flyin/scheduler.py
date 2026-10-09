"""Plan every drone's route through a shared booking calendar."""

from flyin.graph import Network

Route = list[tuple[str, int]]


class Scheduler:
    """Planner that books zones and links turn by turn."""

    def __init__(self, network: Network) -> None:
        """Start with an empty calendar for the given network."""
        raise NotImplementedError

    def plan(self) -> list[Route]:
        """Return one route per drone, in drone order."""
        raise NotImplementedError

    def _search(self) -> Route:
        """Return the earliest-arriving route for the next drone."""
        raise NotImplementedError

    def _zone_has_room(self, zone: str, turn: int) -> bool:
        """Return True if ``zone`` can take one more drone at ``turn``."""
        raise NotImplementedError

    def _link_has_room(self, a: str, b: str, turn: int) -> bool:
        """Return True if one more drone can start crossing ``a-b``."""
        raise NotImplementedError

    def _book(self, route: Route) -> None:
        """Reserve every zone and link slot the route uses."""
        raise NotImplementedError
