from openpyxl import Workbook


def generate_excel(summary, room_data, invigilators):
    wb = Workbook()

    # ------------------ Summary Sheet ------------------
    summary_sheet = wb.active
    summary_sheet.title = "Summary"

    summary_sheet.append(["Total Rooms", summary["rooms"]])
    summary_sheet.append(["Total Students", summary["students"]])
    summary_sheet.append(["Total Capacity", summary["capacity"]])
    summary_sheet.append(["Students per Bench", summary["students_per_bench"]])
    summary_sheet.append([])

    summary_sheet.append(["Invigilator Allocation"])
    for room, inv in invigilators.items():
        summary_sheet.append([room, inv])

    # ------------------ Room Sheets ------------------
    for room_name, data in room_data.items():
        sheet = wb.create_sheet(title=room_name)

        grid = data["grid"]
        structured = data["structured"]

        # 🔹 Grid Layout
        sheet.append(["Seating Layout"])
        for row in grid:
            sheet.append(row)

        sheet.append([])

        # 🔹 Structured Table
        sheet.append(["Structured Data"])
        sheet.append(["Room", "Row", "Column", "Roll Number"])

        for item in structured:
            sheet.append([
                item["Room"],
                item["Row"],
                item["Column"],
                item["Roll Number"]
            ])

    return wb