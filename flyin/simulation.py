"""Turn-by-turn simulation engine that enforces occupancy rules."""

from flyin.graph import Network
from flyin.scheduler import Route


class Simulation:
    """Printer that turns planned routes into one output line per turn."""

    def __init__(self, network: Network, routes: list[Route]) -> None:
        """Store the network and one route per drone."""
        self.network = network
        self.routes = routes

    def lines(self) -> list[str]:
        """Return the movements of every turn, one line per turn."""
        raise NotImplementedError
