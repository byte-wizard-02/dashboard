import streamlit as st
from utils.metrics import display_metric_with_target

def render_sales_dashboard(data, role):
    with st.spinner("Loading Sales Dashboard..."):
        st.markdown("## 🟦 Sales Metrics")

        # --- Organized Sales Categories ---

        st.subheader("📌 Lead Generation")
        lead_metrics = [
            ("New Leads", "Number of New Leads/Prospects Added"),
            ("Referrals", "Referral or Partner Introductions"),
            ("CRM Activity", "CRM Activity Logged"),
            ("Content Engagement", "Marketing/Content Engagement"),
        ]
        cols = st.columns(4)
        for i, (metric, label) in enumerate(lead_metrics):
            display_metric_with_target(cols[i % 4], data, metric, label)

        st.subheader("💬 Client Engagement")
        engagement_metrics = [
            ("Meetings Booked", "Client Meetings Booked"),
            ("Discovery Calls", "Discovery Calls Conducted"),
            ("Proposals Sent", "Proposals/Quotes Sent"),
            ("Follow-ups", "Follow-ups Made"),
        ]
        cols = st.columns(4)
        for i, (metric, label) in enumerate(engagement_metrics):
            display_metric_with_target(cols[i % 4], data, metric, label)

        st.subheader("💼 Pipeline Performance")
        pipeline_metrics = [
            ("Deals Closed", "Deals Closed"),
            ("Revenue Closed", "Revenue Closed"),
            ("Sales Cycle Length", "Sales Cycle Length"),
            ("Conversion Rate", "Conversion Rates"),
            ("Client Acquisition Cost", "Client Acquisition Cost"),
            ("Forecasted Revenue", "Forecasted Revenue"),
        ]
        cols = st.columns(3)
        for i, (metric, label) in enumerate(pipeline_metrics):
            display_metric_with_target(cols[i % 3], data, metric, label)

        # --- Commission Section (Admin Only) ---

        st.markdown("---")
        st.subheader("🧾 Commission Management")
        if role == "Admin":
            commission = st.number_input("Add Commission Amount ($)", min_value=0.0, step=100.0)
            if commission > 0:
                st.success(f"Commission of ${commission:,.2f} added.")
        else:
            st.info("🔐 Only Admins can add commissions.")
