# seating_logic.py

import random


def calculate_capacity(rooms, students_per_bench):
    total_capacity = 0

    for room in rooms:
        total_seats = room["rows"] * room["columns"] * students_per_bench
        room["capacity"] = total_seats
        total_capacity += total_seats

    return total_capacity, rooms


def distribute_students(students, rooms, mode):

    if mode == "Random":
        random.shuffle(students)

    allocation = {}
    index = 0

    for room in rooms:
        capacity = room["capacity"]
        allocation[room["name"]] = students[index:index + capacity]
        index += capacity

    return allocation


def generate_seat_mapping(room, students):
    """
    Simple seat numbering per room
    """

    structured = []

    for i, student in enumerate(students):
        structured.append({
            "Room": room["name"],
            "Seat Number": i + 1,
            "Roll Number": student
        })

    return structured


def assign_invigilators(total_invigilators, rooms):

    room_count = len(rooms)
    distribution = {}

    base = total_invigilators // room_count
    remainder = total_invigilators % room_count

    for i, room in enumerate(rooms):
        assigned = base + (1 if i < remainder else 0)
        distribution[room["name"]] = max(1, assigned)

    return distribution