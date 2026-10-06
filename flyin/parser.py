"""Parse and validate a map file into a Network."""
from flyin.errors import ParseError
from flyin.graph import Network
from flyin.models import Connection, Zone, ZoneType


class MapParser:
    """Reader for the Fly-in map file format."""

    def __init__(self) -> None:
        """Start with an empty parsing state."""
        self._reset()

    def parse_file(self, path: str) -> Network:
        """Read the map at ``path`` and return its Network."""
        self._reset()
        with open(path) as file:
            for line_nb, line in enumerate(file, start=1):
                self._parse_line(line_nb, line)
        return self._build()

    def _reset(self) -> None:
        """Clear everything collected from a previous file."""
        self._nb_drones: int | None = None
        self._start: str | None = None
        self._end: str | None = None
        self._zones: dict[str, Zone] = {}
        self._connections: list[Connection] = []

    def _positive_int(self, line_nb: int, what: str, raw: str) -> int:
        """Convert ``raw`` to an int above zero or raise a ParseError."""
        try:
            int_raw = int(raw)
        except ValueError:
            raise ParseError(
                line_nb, f"{what} must be an integer, got {raw!r}")
        if not int_raw > 0:
            raise ParseError(
                line_nb, f"{what} must be positive, got {int_raw!r}")
        return int_raw

    def _parse_line(self, line_nb: int, line: str) -> None:
        """Dispatch one line of the file by its prefix."""
        raw_line = line.rstrip("\n")
        line = line.partition("#")[0].strip()
        if not line:
            return
        prefix, _, rest = line.partition(":")

        if self._nb_drones is None and prefix != "nb_drones":
            raise ParseError(
                line_nb, "first line must be 'nb_drones: <number>'")

        if prefix in ("start_hub", "end_hub", "hub"):
            self._parse_zone(line_nb, prefix, rest)

        elif prefix == "nb_drones":
            if self._nb_drones is not None:
                raise ParseError(line_nb, "nb_drones defined twice")
            self._nb_drones = self._positive_int(line_nb, "nb_drones", rest)

        elif prefix == "connection":
            self._parse_connection(line_nb, rest)

        else:
            raise ParseError(line_nb, raw_line)

    def _parse_zone(self, line_nb: int, prefix: str, rest: str) -> None:
        """Parse a ``start_hub``, ``end_hub`` or ``hub`` line."""
        body, _, meta_text = rest.partition("[")
        parts = body.split()
        if len(parts) != 3:
            raise ParseError(line_nb, "incorrect format/ something missing")

        name, x, y = parts
        if "-" in name:
            raise ParseError(line_nb, "forbidden character used")

        try:
            int_x = int(x)
            int_y = int(y)
        except ValueError:
            raise ParseError(line_nb, "coordinate not an integer")
        zone = Zone(name, int_x, int_y)

        meta = self._parse_meta(meta_text)
        if "zone" in meta:
            try:
                zone.zone_type = ZoneType(meta["zone"])
            except ValueError:
                raise ParseError(line_nb, "Invalid zone type")
        if "color" in meta:
            zone.color = meta["color"]
        if "max_drones" in meta and prefix == "hub":
            zone.max_drones = self._positive_int(
                line_nb, "max_drones", meta["max_drones"]
            )

        if name in self._zones:
            raise ParseError(line_nb, f"duplicate zone name {name!r}")
        self._zones[name] = zone
        if prefix == "start_hub":
            if self._start is not None:
                raise ParseError(line_nb, "start_hub defined twice")
            self._start = name
        elif prefix == "end_hub":
            if self._end is not None:
                raise ParseError(line_nb, "end_hub defined twice")
            self._end = name

    def _parse_connection(self, line_nb: int, rest: str) -> None:
        """Parse a ``connection: a-b`` line."""
        body, _, meta_text = rest.partition("[")
        a, b = body.strip().split("-")
        connection = Connection(a, b)

        meta = self._parse_meta(meta_text)
        if "max_link_capacity" in meta:
            connection.capacity = int(meta["max_link_capacity"])

        self._connections.append(connection)

    def _parse_meta(self, meta_text: str) -> dict[str, str]:
        """Turn ``key=value key=value]`` into a dict."""
        meta: dict[str, str] = {}
        for item in meta_text.rstrip("]").split():
            key, _, value = item.partition("=")
            meta[key] = value
        return meta

    def _build(self) -> Network:
        """Create the Network from everything collected."""
        if self._nb_drones is None:
            raise ParseError(1, "file has no nb_drones line")
        if self._start is None:
            raise ParseError(1, "start_hub is missing")
        if self._end is None:
            raise ParseError(1, "end_hub is missing")
        network = Network(self._nb_drones, self._start, self._end)
        for zone in self._zones.values():
            network.add_zone(zone)
        for connection in self._connections:
            network.add_connection(connection)
        return network
