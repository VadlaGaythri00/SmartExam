# excel_generator.py

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from io import BytesIO


def generate_excel(summary_data, structured_data, invigilators):

    wb = Workbook()

    # ---------------- MAIN SHEET (SEATING FIRST) ----------------
    ws_main = wb.active
    ws_main.title = "Seating_Arrangement"

    ws_main.append(["Room", "Seat Number", "Roll Number"])

    # Combine all rooms into one sheet
    for room_name in structured_data:
        df = pd.DataFrame(structured_data[room_name])

        for row in dataframe_to_rows(df, index=False, header=False):
            ws_main.append(row)

    # ---------------- SUMMARY SHEET ----------------
    ws_summary = wb.create_sheet(title="Summary")

    ws_summary.append(["SmartExam - Examination Seating Summary"])
    ws_summary.append([])

    for key, value in summary_data.items():
        ws_summary.append([key, value])

    ws_summary.append([])
    ws_summary.append(["Invigilator Distribution"])

    for room, inv in invigilators.items():
        ws_summary.append([room, inv])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return output