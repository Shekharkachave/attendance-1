import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Student Attendance Dashboard", layout="centered")
st.title("🎓 Student Attendance Dashboard")

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
        prn_list = df[prn_column].unique()
        selected_prn = st.selectbox("🔍 Select PRN Number", prn_list)

        # Get all subject columns
        subject_cols = [col for col in df.columns if col not in [prn_column, name_column]]

        st.markdown("### 🧮 Enter Total Lectures for Each Subject")
