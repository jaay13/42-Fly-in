"""Entry point: parse a map file, plan routes, run and print the simulation."""

import sys

from flyin import FlyInError, MapParser


class FlyIn:
    def run(self):
        if len(sys.argv) == 2:
            try:
                network = MapParser().parse_file(sys.argv[1])
            except (FlyInError, OSError) as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            else:
                print(f"Number of Drones: {network.nb_drones}")
                print(network.start)
                print(network.end)
                for zones in network.zones.values():
                    print(zones)
                for connections in network.connections.values():
                    print(connections)
        else:
            print("usage: python3 fly_in.py <map_file>", file=sys.stderr)
            sys.exit(1)        


if __name__ == "__main__":
    FlyIn().run()