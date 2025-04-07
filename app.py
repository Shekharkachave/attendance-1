
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
import os

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Attendance Data File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    return file_path

def analyze_attendance(df, prn):
    df["PRN"] = df["PRN"].astype(str).str.lower()
    prn = prn.lower()
    student_df = df[df["PRN"] == prn]

    if student_df.empty:
        return None, None, None

    total_lectures = len(student_df)
    absences = student_df["Attendance"].value_counts().get("Absent", 0)
    attendance_percentage = ((total_lectures - absences) / total_lectures) * 100

    labels = ["Present", "Absent"]
    sizes = [total_lectures - absences, absences]
    colors = ['#4CAF50', '#F44336']

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.title(f"Attendance for PRN: {prn.upper()}")
    plt.axis("equal")
    plt.show()

    missed_lectures = student_df[student_df["Attendance"] == "Absent"]
    missed_dates = missed_lectures["Date"].tolist()
    missed_subjects = missed_lectures["Subject"].tolist()

    weekday_counts = student_df[student_df["Attendance"] == "Absent"]["Day"].value_counts()
    most_absent_day = weekday_counts.idxmax() if not weekday_counts.empty else "N/A"

    student_data = {
        "PRN": prn.upper(),
        "Total Lectures": total_lectures,
        "Absences": absences,
        "Attendance Percentage": attendance_percentage,
        "Missed Dates": missed_dates,
        "Missed Subjects": missed_subjects,
        "Most Absent Day": most_absent_day,
    }

    return student_data, missed_lectures, most_absent_day

def main():
    print("Please select your attendance data Excel file.")
    file_path = select_file()

    if not file_path:
        print("No file selected. Exiting...")
        return

    try:
        df = pd.read_excel(file_path)
        expected_columns = {"PRN", "Date", "Subject", "Attendance", "Day"}
        if not expected_columns.issubset(df.columns):
            print(f"Invalid Excel format. Expected columns: {expected_columns}")
            return

        prn = input("Enter the PRN of the student: ").strip()
        student_data, missed_lectures, most_absent_day = analyze_attendance(df, prn)

        if student_data is None:
            print(f"No data found for PRN: {prn}")
            return

        print(f"\nStudent Details:\nPRN: {student_data['PRN']}")
        print(f"Total Lectures: {student_data['Total Lectures']}")
        print(f"Absences: {student_data['Absences']}")
        print(f"Attendance Percentage: {student_data['Attendance Percentage']:.2f}%")

        if student_data['Missed Dates']:
            print("\nMissed Lectures:")
            print("Date | Subject")
            print("-" * 25)
            for i in range(len(student_data["Missed Dates"])):
                print(f"{student_data['Missed Dates'][i]} | {student_data['Missed Subjects'][i]}")
        else:
            print("\nNo missed lectures!")

        if not missed_lectures.empty:
            filename = f"{student_data['PRN']}_missed_lectures.csv"
            missed_lectures.to_csv(filename, index=False)
            print(f"\nMissed lectures exported to '{filename}'")

        print(f"\nMost Absent Day: {most_absent_day}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please ensure your Excel file has the correct format with columns: PRN, Date, Subject, Attendance, Day")

if __name__ == "__main__":
    main()
