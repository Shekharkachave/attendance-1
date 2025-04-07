import pandas as pd
import matplotlib.pyplot as plt

# Function to load the Excel file
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

# Function to calculate attendance for the student (PRN or Name) and visualize it
def calculate_attendance(df, prn_or_name):
    # Filter data based on the entered PRN or Name
    student_df = df[df["PRN"].str.lower() == prn_or_name.lower()]
    
    if student_df.empty:
        print(f"No data found for {prn_or_name}.")
        return

    # Calculate overall attendance percentage
    total_lectures = len(student_df)
    absences = student_df["Attendance"].value_counts().get("Absent", 0)
    attendance_percentage = ((total_lectures - absences) / total_lectures) * 100

    print(f"\nAttendance for PRN or Name: {prn_or_name.upper()}")
    print(f"Total Lectures: {total_lectures}")
    print(f"Absences: {absences}")
    print(f"Attendance Percentage: {attendance_percentage:.2f}%")

    # Pie chart for overall attendance (Present vs Absent)
    overall_labels = ["Present", "Absent"]
    overall_sizes = [total_lectures - absences, absences]
    overall_colors = ['#4CAF50', '#F44336']

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    ax[0].pie(overall_sizes, labels=overall_labels, autopct="%1.1f%%", startangle=90, colors=overall_colors)
    ax[0].set_title(f"Overall Attendance for {prn_or_name.upper()}")
    ax[0].axis("equal")

    # Subject-wise attendance (Bar chart)
    print("\nSubject-wise Attendance:")
    subject_attendance = student_df.groupby("Subject")["Attendance"].value_counts().unstack().fillna(0)

    # Plotting subject-wise attendance bar chart
    subject_attendance['Present'] = subject_attendance['Present'].astype(int)
    subject_attendance['Absent'] = subject_attendance['Absent'].astype(int)
    
    subject_attendance.plot(kind='bar', stacked=True, ax=ax[1], color=['#4CAF50', '#F44336'])
    ax[1].set_title(f"Subject-wise Attendance for {prn_or_name.upper()}")
    ax[1].set_xlabel("Subjects")
    ax[1].set_ylabel("Attendance Count")
    ax[1].legend(title="Attendance", labels=["Present", "Absent"])

    # Show the graphs
    plt.tight_layout()
    plt.show()

# Main function
def main():
    # File path for the Excel file (make sure it has columns: PRN, Subject, Attendance)
    file_path = input("Enter the path to the Excel file: ")
    
    # Load data
    df = load_data(file_path)
    if df is None:
        return
    
    # Prompt user for PRN or Name
    prn_or_name = input("Enter the PRN or Name of the student: ").strip()

    # Calculate and display attendance data with graphs
    calculate_attendance(df, prn_or_name)

if __name__ == "__main__":
    main()
