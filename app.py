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
    df.columns = df.columns.str.strip()  # remove leading/trailing spaces from column names

    # 🔍 Auto-detect the PRN column (case-insensitive search)
    prn_column = next((col for col in df.columns if 'prn' in col.lower()), None)

    if not prn_column:
        st.error("❌ No column containing 'PRN' found. Please check your Excel format.")
        st.write("📄 Detected columns:", df.columns.tolist())  # Debug info for the user
    else:
        # PRN dropdown
        prn_list = df[prn_column].unique()
        selected_prn = st.selectbox("🔍 Select PRN Number", prn_list)

        # Filter data for selected PRN
        student_data = df[df[prn_column] == selected_prn]

        if student_data.empty:
            st.warning("⚠️ No data found for the selected PRN.")
        else:
            st.subheader(f"📄 Attendance Report for PRN: `{selected_prn}`")

            # Drop PRN column to focus only on subjects
            subject_data = student_data.drop(columns=[prn_column])
            present_counts = subject_data.iloc[0]

            # Adjust this if total lectures per subject vary
            total_lectures = 100  
            attendance_percentages = (present_counts / total_lectures) * 100

            # Subject-wise Attendance Bar Chart
            st.markdown("### 📊 Subject-wise Attendance")
            fig_bar, ax = plt.subplots(figsize=(8_
