"""Entry point: parse a map file, plan routes, run and print the simulation."""

import sys

from flyin import FlyInError, MapParser, Scheduler, Simulation


class FlyIn:
    """Command-line front end of the program."""

    def run(self) -> None:
        """Load the map named in ``sys.argv`` and print it."""
        if len(sys.argv) == 2:
            try:
                network = MapParser().parse_file(sys.argv[1])
                routes = Scheduler(network).plan()
            except (FlyInError, OSError) as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            else:
                simulation = Simulation(network, routes)
                for line in simulation.lines():
                    print(line)
        else:
            print("usage: python3 fly_in.py <map_file>", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    FlyIn().run()
