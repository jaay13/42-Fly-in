*This project has been created as part of the 42 curriculum by <login>.*

# Fly-in

## Description

Fly-in routes a fleet of drones from a start hub to an end hub through a
network of zones and connections, in as few simulation turns as possible.

Each map sets the number of drones, the zones with their coordinates and type,
and the connections between them. Zones and connections can only hold a
limited number of drones at the same time. Zone types change how drones move:

| Type | Effect |
|---|---|
| `normal` | entering takes 1 turn |
| `priority` | entering takes 1 turn |
| `restricted` | entering takes 2 turns; the drone is in flight on the connection in between |
| `blocked` | cannot be entered |

The program parses and validates the map, plans a route for every drone
without breaking any capacity, and prints the simulation turn by turn.

## Instructions

Requires Python 3.10 or later.

```bash
make install                        # install flake8, mypy and pytest
make run                            # run the default map
make run MAP=maps/hard/02_capacity_hell.txt
python3 fly_in.py <map_file>        # same thing without make
```

Other rules:

| Rule | What it does |
|---|---|
| `make debug` | run under `pdb` |
| `make lint` | `flake8` and `mypy` with the flags required by the subject |
| `make lint-strict` | `flake8` and `mypy --strict` |
| `make test` | run the test suite |
| `make clean` | remove `__pycache__`, `.mypy_cache` and `.pytest_cache` |

An invalid map prints `Error: line N: <reason>` to stderr and exits with
status 1. A map where the end cannot be reached prints
`Error: no path from '<start>' to '<end>'` and exits with status 1.

## Algorithm

TODO

## Visual representation

TODO

## Example

TODO

## Resources

- Python documentation: [`heapq`](https://docs.python.org/3/library/heapq.html),
  [`dataclasses`](https://docs.python.org/3/library/dataclasses.html),
  [`enum`](https://docs.python.org/3/library/enum.html)
- [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Multi-agent pathfinding](https://en.wikipedia.org/wiki/Multi-agent_pathfinding),
  in particular cooperative A* with a reservation table
- [mypy documentation](https://mypy.readthedocs.io/)

### AI usage

Claude (Anthropic) was used as a tutor and assistant:

- **Explanations:** BFS versus DFS, time-expanded search, the booking
  calendar and `heapq`, through interactive step-through pages that run on
  this project's own code and maps.
- **Reviews:** pointing out bugs and edge cases in my code as hints, without
  writing the logic. All parsing, pathfinding and scheduling logic is my own.
- **Repetitive work:** docstrings, flake8 and mypy fixes, the test suite and
  test maps, and commit messages.
