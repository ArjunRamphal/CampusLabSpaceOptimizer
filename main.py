"""Assign modules to compatible computer labs and compare two search stages."""

import argparse
from pathlib import Path
import time


BASE_DIR = Path(__file__).resolve().parent

def load_labs(filename):
    labs = {}

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")

            lab_id = parts[0]
            name = parts[1]
            capacity = int(parts[2])
            software = set(parts[3].split())

            labs[lab_id] = {
                "name": name,
                "capacity": capacity,
                "software": software
            }

    return labs

def load_modules(filename):
    modules = {}

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")

            module_id = parts[0]
            name = parts[1]
            students = int(parts[2])
            software = parts[3]

            modules[module_id] = {
                "name": name,
                "students": students,
                "software": software
            }

    return modules

def is_feasible(module_id, lab_id):
    module = modules[module_id]
    lab = labs[lab_id]

    if module["students"] > lab["capacity"]:
        return False

    if module["software"] not in lab["software"]:
        return False

    return True

def total_unused_seats(assignment):
    total = 0
    for module_id, lab_id in assignment.items():
        students = modules[module_id]["students"]
        capacity = labs[lab_id]["capacity"]
        total += capacity - students
    return total

def greedy_assignment():
    assignment = {}

    sorted_modules = sorted(modules.keys(),
                            key=lambda m: modules[m]["students"],
                            reverse=True)

    for module_id in sorted_modules:
        feasible_labs = []

        for lab_id in labs:
            if is_feasible(module_id, lab_id):
                feasible_labs.append(lab_id)

        if not feasible_labs:
            raise ValueError(f"No feasible lab found for {module_id}")

        best_lab = min(feasible_labs,
                       key=lambda l: labs[l]["capacity"])

        assignment[module_id] = best_lab

    return assignment

def local_search(initial_assignment):
    current_assignment = initial_assignment.copy()
    improved = True

    while improved:
        improved = False

        for module_id in modules:
            current_lab = current_assignment[module_id]

            for lab_id in labs:
                if lab_id == current_lab:
                    continue

                if not is_feasible(module_id, lab_id):
                    continue

                new_assignment = current_assignment.copy()
                new_assignment[module_id] = lab_id

                if total_unused_seats(new_assignment) < total_unused_seats(current_assignment):
                    current_assignment = new_assignment
                    improved = True
                    break

            if improved:
                break

    return current_assignment

def print_solution(title, assignment):
    print(title)

    # Group modules by lab
    lab_groups = {lab_id: [] for lab_id in labs}

    for module_id, lab_id in assignment.items():
        lab_groups[lab_id].append(module_id)

    total_unused = 0

    for lab_id, module_list in lab_groups.items():
        lab = labs[lab_id]

        print(f"\n{lab_id} - {lab['name']}")

        if not module_list:
            print("  No modules assigned.")
            continue

        for module_id in module_list:
            module = modules[module_id]
            unused = lab["capacity"] - module["students"]
            total_unused += unused

            print(f"  {module_id} ({module['name']})")
            print(f"     Students: {module['students']}")
            print(f"     Unused Seats: {unused}")

    print("\n")
    print(f"TOTAL UNUSED SEATS: {total_unused}")
    print("\n")

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--labs",
        type=Path,
        default=BASE_DIR / "data" / "Labs.txt",
        help="Lab input file (default: data/Labs.txt beside this script).",
    )
    parser.add_argument(
        "--modules",
        type=Path,
        default=BASE_DIR / "data" / "Modules.txt",
        help="Module input file (default: data/Modules.txt beside this script).",
    )
    args = parser.parse_args(argv)

    global labs, modules
    try:
        labs = load_labs(args.labs)
        modules = load_modules(args.modules)
    except (OSError, ValueError, IndexError) as error:
        parser.error(f"Could not load input data: {error}")

    start_greedy = time.perf_counter()
    try:
        greedy_solution = greedy_assignment()
    except ValueError as error:
        parser.error(str(error))
    end_greedy = time.perf_counter()

    greedy_time = end_greedy - start_greedy

    start_local = time.perf_counter()
    improved_solution = local_search(greedy_solution)
    end_local = time.perf_counter()

    local_time = end_local - start_local

    print_solution("GREEDY SOLUTION", greedy_solution)
    print_solution("IMPROVED SOLUTION", improved_solution)

    print("Processing Times")
    print(f"Greedy Algorithm Time: {greedy_time:.6f} seconds")
    print(f"Local Search Time: {local_time:.6f} seconds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
