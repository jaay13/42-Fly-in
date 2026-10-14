"""Entry point: parse a map file, plan routes, run and print the simulation."""

import sys

from flyin import (Display, FlyInError, MapParser, MapView, Scheduler,
                   Simulation)


class FlyIn:
    """Command-line front end of the program."""

    def run(self) -> None:
        """Run the program; exit with 130 and no traceback on Ctrl-C."""
        try:
            self._run()
        except KeyboardInterrupt:
            print(file=sys.stderr)
            sys.exit(130)

    def _run(self) -> None:
        """Plan the map in ``sys.argv``; print each turn or animate it."""
        visual = len(sys.argv) == 3 and sys.argv[2] == "--visual"
        if len(sys.argv) == 2 or visual:
            try:
                network = MapParser().parse_file(sys.argv[1])
                routes = Scheduler(network).plan()
            except (FlyInError, OSError) as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            else:
                simulation = Simulation(network, routes)
                if visual:
                    MapView(network, simulation).play()
                else:
                    display = Display(network, sys.stdout.isatty())
                    for line in simulation.lines():
                        print(display.paint(line))
        else:
            print("usage: python3 fly_in.py <map_file> [--visual]",
                  file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    FlyIn().run()
