import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Student Attendance Dashboard", layout="centered")
st.title("🎓 Student Attendance Dashboard")

uploaded_file = st.file_uploader("📤 Upload Attendance Excel File", type=["xlsx"])

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip()  # Clean column names

    # Identify PRN and Name columns
    prn_column = next((col for col in df_raw.columns if 'prn' in col.lower()), None)
    name_column = next((col for col in df_raw.columns if 'name' in col.lower()), None)

    if not prn_column:
        st.error("❌ No 'PRN' column found in the Excel file.")
    else:
        # Extract total lectures from the first row (assuming it’s labeled "Total")
        total_row = df_raw[df_raw[prn_column].astype(str).str.lower() == 'total']
        df = df_raw[df_raw[prn_column].astype(str).str.lower() != 'total']

        if total_row.empty:
            st.error("❌ Could not find a row labeled 'Total' to get lecture counts.")
        else:
            total_lectures = total_row.iloc[0]

            prn_list = df[prn_column].unique()
            selected_prn = st.selectbox("🔍 Select PRN Number", prn_list)

            student_data = df[df[prn_column] == selected_prn]

            if student_data.empty:
                st.warning("⚠️ No data found for the selected PRN.")
            else:
                student_name = student_data.iloc[0][name_column] if name_column else "Name not found"

                st.subheader(f"📄 Attendance Report for PRN: `{selected_prn}`")
                st.markdown(f"**👤 Student Name:** `{student_name}`")

                # Drop PRN and Name to isolate subject columns
                subject_cols = [col for col in df.columns if col not in [prn_column, name_column]]
                present_counts = student_data[subject_cols].iloc[0]
                total_counts = total_lectures[subject_cols].astype(float)

                # Compute percentages
                attendance_percentages = (present_counts / total_counts) * 100

                # Bar Chart
                st.markdown("### 📊 Subject-wise Attendance")
                fig_bar, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(x=attendance_percentages.index, y=attendance_percentages.values, palette="viridis", ax=ax)
                ax.set_ylabel("Attendance %")
                ax.set_ylim(0, 100)
                plt.xticks(rotation=45)
                st.pyplot(fig_bar)

                # Pie Chart - Overall
                total_present = present_counts.sum(skipna=True)
                total_possible = total_counts.sum(skipna=True)
                total_absent = total_possible - total_present

                st.markdown("### 🥧 Overall Attendance Pie Chart")
                fig_pie, ax = plt.subplots()
                ax.pie(
                    [total_present, total_absent],
                    labels=["Present", "Absent"],
                    autopct='%1.1f%%',
                    colors=['#4CAF50', '#F44336']
                )
                ax.axis("equal")
                st.pyplot(fig_pie)

                # Metric
                overall_attendance = (total_present / total_possible) * 100 if total_possible > 0 else 0
                st.metric(label="📈 Overall Attendance", value=f"{overall_attendance:.2f}%")
