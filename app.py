import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("Student Attendance Analyzer")

uploaded_file = st.file_uploader("Upload your attendance Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        expected_columns = {"PRN", "Date", "Subject", "Attendance", "Day"}
        if not expected_columns.issubset(df.columns):
            st.error(f"Invalid Excel format. Expected columns: {expected_columns}")
        else:
            prn = st.text_input("Enter the PRN of the student").strip()
            if prn:
                df["PRN"] = df["PRN"].astype(str).str.lower()
                prn = prn.lower()
                student_df = df[df["PRN"] == prn]

                if student_df.empty:
                    st.warning("No data found for this PRN.")
                else:
                    total_lectures = len(student_df)
                    absences = student_df["Attendance"].value_counts().get("Absent", 0)
                    attendance_percentage = ((total_lectures - absences) / total_lectures) * 100

                    labels = ["Present", "Absent"]
                    sizes = [total_lectures - absences, absences]
                    colors = ['#4CAF50', '#F44336']

                    fig, ax = plt.subplots()
                    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
                    ax.set_title(f"Attendance for PRN: {prn.upper()}")
                    ax.axis("equal")
                    st.pyplot(fig)

                    missed_lectures = student_df[student_df["Attendance"] == "Absent"]
                    missed_dates = missed_lectures["Date"].tolist()
                    missed_subjects = missed_lectures["Subject"].tolist()

                    weekday_counts = missed_lectures["Day"].value_counts()
                    most_absent_day = weekday_counts.idxmax() if not weekday_counts.empty else "N/A"

                    st.subheader("Summary")
                    st.markdown(f"**Total Lectures:** {total_lectures}")
                    st.markdown(f"**Absences:** {absences}")
                    st.markdown(f"**Attendance Percentage:** {attendance_percentage:.2f}%")
                    st.markdown(f"**Most Absent Day:** {most_absent_day}")

                    if missed_lectures.empty:
                        st.success("No missed lectures!")
                    else:
                        st.subheader("Missed Lectures")
                        st.dataframe(missed_lectures[["Date", "Subject"]])

                        # Create downloadable CSV
                        csv = missed_lectures.to_csv(index=False).encode('utf-8')
                        st.download_button("Download Missed Lectures CSV", data=csv, file_name=f"{prn.upper()}_missed_lectures.csv", mime="text/csv")
    except Exception as e:
        st.error(f"An error occurred: {e}")
