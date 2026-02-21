import streamlit as st
import pandas as pd
from seating_logic import *
from excel_generator import *
from io import BytesIO

st.set_page_config(page_title="SmartExam", layout="wide")

st.title("📚 SmartExam – Intelligent Examination Seating System")

# ---------------- SIDEBAR CONFIG ---------------- #

st.sidebar.header("Room Configuration")

num_rooms = st.sidebar.number_input(
    "Number of Rooms",
    min_value=1,
    value=1
)

rooms = []

for i in range(num_rooms):
    st.sidebar.subheader(f"Room {i+1}")

    name = st.sidebar.text_input(
        f"Room Name {i+1}",
        value=f"Room{i+1}"
    )

    rows = st.sidebar.number_input(
        f"Rows (Room {i+1})",
        min_value=1,
        value=5
    )

    columns = st.sidebar.number_input(
        f"Columns (Room {i+1})",
        min_value=1,
        value=5
    )

    rooms.append({
        "name": name,
        "rows": rows,
        "columns": columns
    })

students_per_bench = st.sidebar.selectbox(
    "Students per Bench",
    [1]
)

invigilators = st.sidebar.number_input(
    "Total Invigilators",
    min_value=1,
    value=1
)

mode = st.sidebar.selectbox(
    "Seating Mode",
    ["Sequential", "Random"]
)

# ---------------- STUDENT INPUT ---------------- #

st.header("Student Roll Numbers")

roll_input = st.text_area(
    "Enter Roll Numbers (comma or line separated)"
)

# ---------------- GENERATE BUTTON ---------------- #

if st.button("Generate Seating Plan"):

    roll_numbers = [
        r.strip()
        for r in roll_input.replace(",", "\n").split("\n")
        if r.strip()
    ]

    total_students = len(roll_numbers)

    total_capacity, room_capacities = calculate_capacity(
        rooms,
        students_per_bench
    )

    if total_students > total_capacity:
        st.error("❌ Students exceed total room capacity!")
        st.stop()

    allocation = distribute_students(
        roll_numbers,
        room_capacities,
        mode
    )

    inv_map = assign_invigilators(
        invigilators,
        rooms
    )

    room_output = {}
    all_structured = []

    for room in rooms:
        grid, structured = generate_grid(
            room["name"],
            allocation[room["name"]],
            room["rows"],
            room["columns"]
        )

        room_output[room["name"]] = {
            "grid": grid,
            "structured": structured
        }

        all_structured.extend(structured)

    # ---------------- SUMMARY ---------------- #

    st.success("✅ Seating Plan Generated Successfully!")

    st.subheader("📊 Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", total_students)
    col2.metric("Total Capacity", total_capacity)
    col3.metric("Unallocated Seats", total_capacity - total_students)

    # ---------------- INVIGILATORS ---------------- #

    st.subheader("👨‍🏫 Invigilator Allocation")

    inv_df = pd.DataFrame(
        list(inv_map.items()),
        columns=["Room", "Invigilator"]
    )

    st.table(inv_df)

    # ---------------- SEATING ARRANGEMENT ---------------- #

    st.subheader("🪑 Seating Arrangement (Row × Column View)")

    for room_name, data in room_output.items():
        st.markdown(f"### {room_name}")

        seating_df = pd.DataFrame(data["grid"])
        st.table(seating_df)

    # ---------------- EXCEL GENERATION ---------------- #

    summary_data = {
        "rooms": num_rooms,
        "students": total_students,
        "capacity": total_capacity,
        "students_per_bench": students_per_bench
    }

    wb = generate_excel(summary_data, room_output, inv_map)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    st.subheader("📥 Excel Options")

    view_excel = st.button("View Excel Data")

    if view_excel:
        st.dataframe(pd.DataFrame(all_structured))

    st.download_button(
        label="Download Excel File",
        data=buffer,
        file_name="SmartExam_Seating.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )