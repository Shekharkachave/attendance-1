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
    df.columns = df.columns.str.strip()  # remove extra spaces

    # Auto-detect PRN column
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
            # Auto-detect name column
            name_column = next((col for col in df.columns if 'name' in col.lower()), None)
            student_name = student_data.iloc[0][name_column] if name_column else "Name not found"

            st.subheader(f"📄 Attendance Report for PRN: `{selected_prn}`")
            st.markdown(f"**👤 Student Name:** `{student_name}`")

            # Drop PRN and Name columns, convert rest to numeric
            drop_cols = [prn_column]
            if name_column:
                drop_cols.append(name_column)

            subject_data = student_data.drop(columns=drop_cols)
            subject_data =_
