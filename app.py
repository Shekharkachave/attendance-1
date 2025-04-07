import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page setup
st.set_page_config(page_title="Student Attendance Dashboard", layout="centered")
st.title("🎓 Student Attendance Dashboard")

# Upload Excel File
uploaded_file = st.file_uploader("📤 Upload Attendance Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # Clean column names

    # Detect PRN and Name columns
    prn_column = next((col for col in df.columns if 'prn' in col.lower()), None)
    name_column = next((col for col in df.columns if 'name' in col.lower()), None)

    if not prn_column:
        st.error("❌ 'PRN' column not found in the uploaded Excel file.")
    else:
        # Find and extract total lectures row
        total_row = df[df[prn_column].astype(str).str.lower() == 'total']
        if total_row.empty:
            st.error("❌ Could not find a row labeled 'Total' to get lecture counts.")
        else:
            total_counts = total_row.iloc[0]
            df = df[df[prn_column].astype(str).str.lower() != 'total']  # remove 'Total' row

            prn_list = df[prn_column].unique()
            selected_prn = st.selectbox("🔍 Select PRN Number", prn_list)

            subject_cols = [col for col in df.columns if col not in [prn_column, name_column]]

            student_data = df[df[prn_column] == selected_prn]

            if student_data.empty:
                st.warning("⚠️ No data found for the selected PRN.")
            else:
                student_name = student_data.iloc[0][name_column] if name_column else "N/A"
                st.subheader(f"📄 Attendance Report for PRN: `{selected_prn}`")
                st.markdown(f"**👤 Student Name:** `{student_name}`")

                present_counts = student_
