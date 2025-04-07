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
            attendance_percentages = (present_counts / total_lectures) * 100

            # Subject-wise Bar Chart
            st.markdown("### 📊 Subject-wise Attendance")
            fig_bar, ax = plt.subplots(figsize=(8, 4))  # ✅ fixed
            sns.barplot(x=attendance_percentages.index, y=attendance_percentages.values, palette="viridis", ax=ax)
            ax.set_ylabel("Attendance %")
            ax.set_ylim(0, 100)
            plt.xticks(rotation=45)
            st.pyplot(fig_bar)

            # Pie Chart
            total_present = present_counts.sum()
            total_possible = total_lectures * len(present_counts)
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

            # Overall metric
            overall_attendance = (total_present / total_possible) * 100
            st.metric(label="📈 Overall Attendance", value=f"{overall_attendance:.2f}%")

else:
    st.info("📁 Please upload an Excel file to begin.")
