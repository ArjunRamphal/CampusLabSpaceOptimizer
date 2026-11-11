# Setup and input files

## Requirements

- Python 3.10 or newer, available as `python`, `python3`, or `py` on Windows.
- No external packages, database, or network service.

The organised repository was checked with Python 3.12.14. Both algorithms completed using the bundled data, and their minimum unused-seat total was checked against all 648 feasible allocations.

## Run with the sample data

From the repository directory:

```bash
python main.py
```

The default files are `data/Labs.txt` and `data/Modules.txt` relative to `main.py`, regardless of the current working directory. For example:

```bash
python /path/to/CampusLabSpaceOptimizer/main.py
```

Both stages should assign all ten modules and report `TOTAL UNUSED SEATS: 140`. Processing times depend on the computer and are not fixed expected values.

## Use another dataset

```bash
python main.py --labs path/to/Labs.txt --modules path/to/Modules.txt
```

Custom relative paths are resolved from the directory where the command is run. Quote paths containing spaces. `--labs` and `--modules` can be overridden independently.

### Lab format

Use four comma-separated fields per line, with no header or blank rows:

```text
LabID,Lab Name,Capacity,Software Installed
```

The line above describes the fields; do not include it in the input file. Actual rows look like:

```text
L1,Advanced Lab A,100,Python Java MATLAB
L2,Coding Lab B,60,Python Java
```

Separate installed software names with spaces. Capacity must be a positive integer. Each lab ID must be unique.

### Module format

Use four comma-separated fields per line, with no header or blank rows:

```text
ModuleID,Module Name,Students,Software Needed
```

Actual rows look like:

```text
M1,AI Systems,85,Python
M2,Control Systems,45,MATLAB
```

Students must be a positive integer and each module ID must be unique. Each module requires one software name, matched exactly and case-sensitively against the lab's installed names. Multiple software requirements per module are not supported.

These files use a simple comma-delimited format rather than a full CSV parser. Avoid commas inside names, whitespace around fields, and quoted fields. The loader expects valid input and does not validate duplicate IDs or positive counts.

## Understanding the model

All modules take place at different times. Capacity is checked separately for each module, and a lab can be reused for any number of modules. There are no room availability, session duration, travel, or scheduling conflict constraints.

The objective sums the unused seats for each module's session. For example, assigning two 25-student modules to the same 30-seat lab contributes `5 + 5 = 10` unused seats across their sessions.

The smallest compatible lab is independently the best choice for each module. Local search consequently returns the same objective value as greedy allocation under this model. Adding shared constraints would require revisiting both the algorithms and this conclusion.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Python command not found | Try `python3` or `py`, or install Python and add it to your PATH. |
| `Could not load input data` | Check the reported path, file permissions, field counts, and integer enrolments/capacities. |
| `No feasible lab found for ...` | Ensure at least one lab has enough seats and an exact match for the required software name. |
| The two algorithms give the same total | Expected: the greedy rule already minimises this model's objective. |

Input failures and infeasible allocations reported by the command return exit status 2. Successful runs return 0. The program reads its input files without modifying them and prints results to the terminal.
