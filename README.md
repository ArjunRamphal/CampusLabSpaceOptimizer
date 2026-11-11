# Campus Lab Space Optimizer

A Python command-line tool that assigns university modules to computer labs with enough seats and the required software. Developed for **COMP719: Optimization and Modelling**, it compares a greedy allocation with hill-climbing local search using the supplied four-lab, ten-module dataset.

## Quick start

Use Python 3.10 or newer. The program uses only the standard library; there are no packages to install.

```bash
git clone https://github.com/ArjunRamphal/CampusLabSpaceOptimizer.git
cd CampusLabSpaceOptimizer
python main.py
```

On systems where Python is named `python3`, use `python3 main.py`. The bundled input paths are resolved relative to the script, so it also works when launched from another directory.

To supply your own files:

```bash
python main.py --labs path/to/Labs.txt --modules path/to/Modules.txt
```

Run `python main.py --help` for the command options. See [setup and input format](docs/SETUP.md) for details.

## How allocation works

Each module must be assigned to exactly one lab. An assignment is feasible when the lab capacity is at least the module's enrolment and the lab has its required software. The objective is to minimise the sum of `lab capacity - module students` over all module assignments.

**Scheduling assumption:** all modules run at different times. A lab can therefore host several modules without sharing its capacity between them. This project allocates rooms; it does not build a timetable or check overlapping sessions.

1. **Greedy allocation** processes modules from largest to smallest and chooses the smallest compatible lab for each one.
2. **Hill-climbing local search** tries moving one module at a time to another feasible lab and accepts a move only if it reduces total unused seats.

Under this model, one module's choice does not affect another's. Choosing the smallest feasible lab for each module already minimises every term in the objective, so the greedy solution is optimal and local search cannot improve it. The second stage is retained to demonstrate the project's required search approach.

## Bundled dataset results

The program prints both allocations grouped by lab, their unused-seat totals, and the execution time for each stage.

| Lab | Assigned modules | Unused seats across assignments |
| --- | --- | ---: |
| L1 - Advanced Lab A | M7, M1, M2 | 80 |
| L2 - Coding Lab B | M4, M10 | 15 |
| L3 - Data Lab C | M5, M8 | 15 |
| L4 - Legacy Lab D | M3, M9, M6 | 30 |
| **Total** | **10 modules** | **140** |

Both stages produce **140 unused seats**, summed over the separate module sessions. This is not a count of seats vacant at one moment. Exhaustive evaluation of all **648 feasible allocations** confirms that 140 is the minimum for the supplied data. Execution times vary by machine.

## Repository layout

| Path | Purpose |
| --- | --- |
| [main.py](main.py) | Input loading, feasibility checks, both algorithms, and console output |
| [data/Labs.txt](data/Labs.txt) | Four sample labs, capacities, and installed software |
| [data/Modules.txt](data/Modules.txt) | Ten sample modules, enrolments, and software requirements |
| [docs/SETUP.md](docs/SETUP.md) | Running the tool, file formats, and troubleshooting |
| [docs/COMP719_Project_Brief.pdf](docs/COMP719_Project_Brief.pdf) | Original university project brief |
| [LICENSE](LICENSE) | MIT license |

## Authors

- Arjun Ramphal
- Darian Robert
- Jerome Reddy
- Keolin Naicker
- Lokadi Naicker
- Preolan Narainsamy
