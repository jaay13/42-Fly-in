"""Exception hierarchy (parse errors with line number, unsolvable map, ...)."""


class FlyInError(Exception):
    """Base class for every expected Fly-in failure."""


class ParseError(FlyInError):
    """A map file broke a format rule."""


class UnsolvableError(FlyInError):
    """The map is valid, but no path joins start_hub to end_hub."""
