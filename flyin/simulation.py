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
        last = max(route[-1][1] for route in self.routes)
        pages: list[list[str]] = [[] for _ in range(last + 1)]

        for drone_id, route in enumerate(self.routes, start=1):
            for (src, depart), (dst, arrive) in zip(route, route[1:]):
                if src == dst:
                    continue
                if arrive - depart == 2:
                    name = self.network.link(src, dst).name
                    pages[depart + 1].append(f"D{drone_id}-{name}")
                pages[arrive].append(f"D{drone_id}-{dst}")

        return [" ".join(page) for page in pages[1:]]
