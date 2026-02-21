# app.py

import streamlit as st
import pandas as pd
from io import BytesIO

from seating_logic import (
    calculate_capacity,
    distribute_students,
    generate_seat_mapping,
    assign_invigilators
)

from excel_generator import generate_excel


st.set_page_config(
    page_title="SmartExam",
    layout="centered"
)

st.title("🎓 SmartExam")
st.caption("Examination Seating Arrangement System")

st.divider()

# ---------------- ROOM CONFIG ----------------

st.subheader("Room Configuration")

num_rooms = st.number_input("Number of Rooms", min_value=1, step=1)

rooms = []

for i in range(num_rooms):
    with st.expander(f"Room {i+1}"):

        name = st.text_input("Room Name/Number", key=f"name_{i}")
        rows = st.number_input("Rows", min_value=1, key=f"rows_{i}")
        columns = st.number_input("Columns", min_value=1, key=f"cols_{i}")

        if name:
            rooms.append({
                "name": name,
                "rows": rows,
                "columns": columns
            })

students_per_bench = st.selectbox("Students per Bench", [1, 2])
total_invigilators = st.number_input("Total Invigilators", min_value=1)
allocation_mode = st.radio("Allocation Mode", ["Sequential", "Random"])

st.divider()

# ---------------- STUDENT INPUT ----------------

st.subheader("Student Roll Numbers")

roll_input = st.text_area("Enter Roll Numbers (comma or line separated)")

students = []

if roll_input:
    raw = roll_input.replace(",", "\n").split("\n")
    students = [r.strip() for r in raw if r.strip()]

# ---------------- GENERATE ----------------

if st.button("Generate Seating Arrangement"):

    if not rooms:
        st.error("Please configure rooms.")
        st.stop()

    if not students:
        st.error("Please enter student roll numbers.")
        st.stop()

    total_capacity, rooms = calculate_capacity(rooms, students_per_bench)

    if len(students) > total_capacity:
        st.error("Students exceed total capacity.")
        st.stop()

    allocation = distribute_students(students, rooms, allocation_mode)

    structured_output = {}

    for room in rooms:
        structured = generate_seat_mapping(
            room,
            allocation[room["name"]]
        )
        structured_output[room["name"]] = structured

    invigilators = assign_invigilators(total_invigilators, rooms)

    summary_data = {
        "Total Rooms": len(rooms),
        "Total Students": len(students),
        "Total Capacity": total_capacity,
        "Students per Bench": students_per_bench
    }

    excel_file = generate_excel(
        summary_data,
        structured_output,
        invigilators
    )

    # 🔥 Store in session state
    st.session_state["structured_output"] = structured_output
    st.session_state["excel_file"] = excel_file

    st.success("Seating Generated Successfully!")
    # ---------------- VIEW OPTION ----------------

if "structured_output" in st.session_state:

    if st.button("👁 View Seating Inside App"):

        for room_name in st.session_state["structured_output"]:
            st.subheader(f"Room {room_name}")
            df = pd.DataFrame(st.session_state["structured_output"][room_name])
            st.dataframe(df, use_container_width=True)

    # ---------------- DOWNLOAD OPTION ----------------

    st.download_button(
        label="⬇ Download Excel File",
        data=st.session_state["excel_file"],
        file_name="SmartExam_Seating_Plan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )