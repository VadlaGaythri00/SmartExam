import random


def calculate_capacity(rooms, students_per_bench):
    total_capacity = 0
    room_capacities = {}

    for room in rooms:
        benches = room["rows"] * room["columns"]
        capacity = benches * students_per_bench
        room_capacities[room["name"]] = capacity
        total_capacity += capacity

    return total_capacity, room_capacities


def distribute_students(roll_numbers, room_capacities, mode):
    if mode == "Random":
        random.shuffle(roll_numbers)

    allocation = {}
    index = 0

    for room, capacity in room_capacities.items():
        allocation[room] = roll_numbers[index:index + capacity]
        index += capacity

    return allocation


def generate_grid(room_name, students, rows, columns):
    grid = []
    structured = []
    student_index = 0

    for r in range(1, rows + 1):
        row_data = []

        for c in range(1, columns + 1):
            if student_index < len(students):
                roll = students[student_index]

                row_data.append(roll)

                structured.append({
                    "Room": room_name,
                    "Row": r,
                    "Column": c,
                    "Roll Number": roll
                })

                student_index += 1
            else:
                row_data.append("")

        grid.append(row_data)

    return grid, structured


def assign_invigilators(num_invigilators, rooms):
    invigilator_map = {}

    for i, room in enumerate(rooms):
        invigilator_map[room["name"]] = f"Invigilator {(i % num_invigilators) + 1}"

    return invigilator_map