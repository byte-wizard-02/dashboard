import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_hr_data
from utils.metrics import display_metric_with_target

def render_hr_dashboard(data):
    with st.spinner("Loading HR Dashboard..."):
        st.markdown("## 🟩 HR Metrics")
        hr_data = load_hr_data()

        # Convert dates
        for col in ['Joining Date', 'Hire Date', 'Application Date']:
            if col in hr_data.columns:
                hr_data[col] = pd.to_datetime(hr_data[col], errors='coerce')

        total_employees = len(hr_data[hr_data['Status'].isin(["Active", "On Leave"])])
        resigned = len(hr_data[hr_data['Status'] == 'Resigned'])
        cost_per_hire = hr_data["Hiring Cost"].mean() if "Hiring Cost" in hr_data.columns else 5000

        if {'Application Date', 'Hire Date'}.issubset(hr_data.columns):
            hr_data["Time to Hire"] = (hr_data["Hire Date"] - hr_data["Application Date"]).dt.days
            time_to_hire = hr_data["Time to Hire"].mean()
        else:
            time_to_hire = 15

        turnover_rate = resigned / len(hr_data) * 100 if len(hr_data) else 0
        retention_rate = 100 - turnover_rate
        revenue_per_employee = data["Revenue Closed"].iloc[-1] / total_employees if total_employees else 0

        offers = len(hr_data[hr_data["Application Status"] == "Offered"]) if "Application Status" in hr_data.columns else 1
        accepted = len(hr_data[hr_data["Application Status"] == "Accepted"]) if "Application Status" in hr_data.columns else 1
        acceptance_rate = accepted / offers * 100 if offers else 0

        internal_promotion_rate = hr_data["Internal Moves"].sum() / total_employees * 100 if total_employees else 0
        overtime_expense = hr_data["Overtime Hours"].sum() * 250 if "Overtime Hours" in hr_data.columns else 25000

        # Engagement Metrics
        training_effectiveness = hr_data["Training Effectiveness"].mean() if "Training Effectiveness" in hr_data.columns else 78
        performance_score = hr_data["Performance Rating"].mean() if "Performance Rating" in hr_data.columns else 82
        satisfaction_score = hr_data["Engagement Score"].mean() if "Engagement Score" in hr_data.columns else 75

        # Core HR Metrics
        st.subheader("📊 Core HR Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Cost per Hire", f"${cost_per_hire:,.0f}")
        col2.metric("Time to Hire", f"{time_to_hire:.1f} days")
        col3.metric("Turnover Rate", f"{turnover_rate:.1f}%")

        col4, col5, col6 = st.columns(3)
        col4.metric("Retention Rate", f"{retention_rate:.1f}%")
        col5.metric("Revenue per Employee", f"${revenue_per_employee:,.0f}")
        col6.metric("Acceptance Rate", f"{acceptance_rate:.1f}%")

        # Diversity & Promotions
        st.subheader("🌍 Diversity & Structure")
        col7, col8, col9 = st.columns(3)
        col7.metric("Internal Promotion Rate", f"{internal_promotion_rate:.1f}%")
        col8.metric("Headcount", total_employees)
        col9.metric("Overtime Expense", f"${overtime_expense:,.0f}")

        # Engagement
        st.subheader("📘 Engagement & Training")
        col10, col11, col12 = st.columns(3)
        col10.metric("Training Effectiveness", f"{training_effectiveness:.1f}%")
        col11.metric("Employee Performance", f"{performance_score:.1f}%")
        col12.metric("Satisfaction Score", f"{satisfaction_score:.1f}")

        # Pie Charts
        if "Gender" in hr_data.columns:
            st.subheader("🧬 Gender Diversity")
            gender_count = hr_data["Gender"].value_counts().reset_index()
            gender_count.columns = ["Gender", "Count"]
            fig = px.pie(gender_count, names="Gender", values="Count", title="Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("🥧 Employee Status Distribution")
        status_count = hr_data["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]
        fig = px.pie(status_count, names="Status", values="Count", title="Employee Status Breakdown")
        st.plotly_chart(fig, use_container_width=True)

        # Revenue per Employee Trend
        st.subheader("📈 Monthly Revenue per Employee")
        monthly_revenue = data.groupby(data['Week'].dt.to_period("M")).agg({
            "Revenue Closed": "sum"
        }).reset_index()
        monthly_revenue["Month"] = monthly_revenue["Week"].astype(str)
        monthly_revenue["Employees"] = total_employees
        monthly_revenue["Revenue per Employee"] = monthly_revenue["Revenue Closed"] / total_employees

        fig = px.line(monthly_revenue, x="Month", y="Revenue per Employee",
                      title="Monthly Revenue per Employee", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # Absenteeism Rate
        st.subheader("📈 Monthly Absenteeism Rate")
        if "Joining Date" in hr_data.columns:
            hr_data["Month"] = hr_data["Joining Date"].dt.to_period("M")
            absent_by_month = hr_data.groupby("Month").apply(
                lambda df: (df["Status"] == "On Leave").sum() / len(df) * 100
            ).reset_index(name="Absenteeism Rate")
            absent_by_month["Month"] = absent_by_month["Month"].astype(str)

            fig = px.line(absent_by_month, x="Month", y="Absenteeism Rate",
                          title="Monthly Absenteeism Rate", markers=True)
            st.plotly_chart(fig, use_container_width=True)

        # Download Button
        st.download_button("⬇️ Download HR Data as CSV", hr_data.to_csv(index=False), file_name="hr_employee_records.csv")

        st.info("🔗 This is demo HR data. Live integration will replace dummy data once API access is connected.")
