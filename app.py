import streamlit as st
import pandas as pd

st.set_page_config(page_title="Attendance Monitor", layout="wide")

st.title("Student Attendance Monitoring")

# Upload file
uploaded_file = st.file_uploader("Upload Attendance Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, index_col=0)
        st.subheader("Raw Attendance Data")
        st.dataframe(df)

        if 'Total' in df.index:
            total_lectures = df.loc['Total']
            df = df.drop(index='Total')  # Remove total row from student records

            st.subheader("Subject-wise Attendance %")
            attendance_percent = (df / total_lectures) * 100
            attendance_percent = attendance_percent.round(2)
            st.dataframe(attendance_percent)

            st.subheader("Overall Attendance %")
            overall_percent = attendance_percent.mean(axis=1).round(2)
            overall_df = pd.DataFrame({
                'Student': overall_percent.index,
                'Overall %': overall_percent.values
            }).set_index('Student')
            st.dataframe(overall_df)

        else:
            st.error("Could not find a row labeled 'Total'. Please check the Excel file format.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an Excel file to begin.")
