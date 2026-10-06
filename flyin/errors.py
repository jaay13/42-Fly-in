"""Fly-in exception hierarchy."""


class FlyInError(Exception):
    """Base class for every expected Fly-in failure."""


class ParseError(FlyInError):
    """A map file broke a format rule."""

    def __init__(self, line_nb: int, message: str) -> None:
        """Store the line number and prefix it to the message."""
        self.line_nb = line_nb
        super().__init__(f"line {line_nb}: {message}")


class UnsolvableError(FlyInError):
    """The map is valid, but no path joins start_hub to end_hub."""
