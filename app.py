import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Student Attendance Dashboard", layout="centered")
st.title("🎓 Student Attendance Dashboard")

# Upload Excel file
uploaded_file = st.file_uploader("📤 Upload Attendance Excel File", type=["xlsx"])

if uploaded_file:
    # Read Excel and clean column names
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # ✅ remove leading/trailing spaces from column names

    # Check if PRN column exists
    if 'PRN' not in df.columns:
        st.error("❌ 'PRN' column not found in the Excel file. Please check the format.")
    else:
        # Dropdown to select PRN
        prn_list = df['PRN'].unique()
        selected_prn = st.selectbox("🔍 Select PRN Number", prn_list)

        # Filter data for selected PRN
        student_data = df[df['PRN'] == selected_prn]

        if student_data.empty:
            st.warning("⚠️ No data found for the selected PRN.")
        else:
            st.subheader(f"📄 Attendance Report for PRN: `{selected_prn}`")

            # Drop PRN to focus on subjects
            subject_data = student_data.drop(columns=['PRN'])
            present_counts = subject_data.iloc[0]

            # Update this if total lectures per subject varies
            total_lectures = 100  
            attendance_percentages = (present_counts / total_lectures) * 100

            # Subject-wise Bar Chart
            st.markdown("### 📊 Subject-wise Attendance")
            fig_bar, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=attendance_percentages.index, y=attendance_percentages.values, palette="viridis", ax=ax)
            ax.set_ylabel("Attendance %")
            ax.set_ylim(0, 100)
            plt.xticks(rotation=45)
            st.pyplot(fig_bar)

            # Overall Attendance Pie Chart
            total_present = present_counts.sum()
            total_possible = total_lectures * len(present_counts)
            total_absent = total_possible - total_present

            st.markdown("### 🥧 Overall Attendance Pie Chart")
            fig_pie, ax = plt.subplots()
            ax.pie([total_present, total_absent], labels=["Present", "Absent"], autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
            ax.axis("equal")
            st.pyplot(fig_pie)

            # Overall Attendance Metric
            overall_attendance = (total_present / total_possible) * 100
            st.metric(label="📈 Overall Attendance", value=f"{overall_attendance:.2f}%")

else:
    st.info("📁 Please upload an Excel file to begin.")
