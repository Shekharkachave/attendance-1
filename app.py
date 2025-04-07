import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel data
@st.cache_data
def load_data():
    return pd.read_excel("attendance_with_subjects.xlsx")

df = load_data()

st.title("🎓 Student Attendance Dashboard")

# Get PRN list
prn_list = df['PRN'].unique()
selected_prn = st.selectbox("Select or Enter PRN Number", prn_list)

# Filter for the selected PRN
student_data = df[df['PRN'] == selected_prn]

if student_data.empty:
    st.warning("No data found for the entered PRN.")
else:
    st.subheader(f"📄 Attendance Details for PRN: {selected_prn}")
    
    # Drop PRN column to focus on subjects
    subject_data = student_data.drop(columns=['PRN'])

    # Count total lectures, present lectures
    present_counts = subject_data.iloc[0]
    total_lectures = 100  # Adjust this if you have per-subject total

    attendance_percentages = (present_counts / total_lectures) * 100

    # Bar chart - Subject-wise Attendance
    st.markdown("### 📊 Subject-wise Attendance")
    fig_bar, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=attendance_percentages.index, y=attendance_percentages.values, palette="viridis", ax=ax)
    ax.set_ylabel("Attendance %")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45)
    st.pyplot(fig_bar)

    # Pie chart - Overall Present vs Absent
    total_present = present_counts.sum()
    total_possible = total_lectures * len(present_counts)
    total_absent = total_possible - total_present

    st.markdown("### 🥧 Overall Attendance Pie Chart")
    fig_pie, ax = plt.subplots()
    ax.pie([total_present, total_absent], labels=["Present", "Absent"], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
    ax.axis("equal")
    st.pyplot(fig_pie)

    # Display overall attendance
    overall_attendance = (total_present / total_possible) * 100
    st.metric(label="📈 Overall Attendance Percentage", value=f"{overall_attendance:.2f}%")

