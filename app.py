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
    df.columns = df.columns.str.strip()  # remove leading/trailing spaces

    # Auto-detect the PRN column
    prn_column = next((col for col in df.columns if 'prn' in col.lower()), None)

    if not prn_column:
        st.error("❌ No column containing 'PRN' found. Please check your Excel format.")
        st.write("📄 Detected columns:", df.columns.tolist())
    else:
        prn_list = df[prn_column].unique()
        selected_prn = st.selectbox("🔍 Select PRN Number", prn_list)

        student_data = df[df[prn_column] == selected_prn]

        if student_data.empty:
            st.warning("⚠️ No data found for the selected PRN.")
        else:
            st.subheader(f"📄 Attendance Report for PRN: `{selected_prn}`")

            # Drop PRN column and extract attendance data
            subject_data = student_data.drop(columns=[prn_column])
            present_counts = subject_data.iloc[0]

            total_lectures = 100  # or update this logic if it varies
            attendance_percentages = (present_counts / total_lectures) * 100  # ✅ Fixed here

            # Subject-wise Bar Chart
            st.markdown("### 📊 Subject-wise Attendance")
            fig_bar, ax = plt.subplots(figsize=(8, 4_
