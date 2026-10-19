import streamlit as st
from utils.metrics import display_metric_with_target

def render_executive_dashboard(data):
    with st.spinner("Loading Executive Overview..."):
        st.markdown("## 🟪 Executive KPIs")

        exec_metrics = [
            ("Strategic Projects", "Strategic Projects Completed"),
            ("Weekly Objectives Met", "Weekly Objectives Met"),
            ("Cross-team Meetings", "Cross-team Meetings"),
            ("Compliance Score", "Compliance Score")
        ]

        cols = st.columns(2)
        for i, (metric, label) in enumerate(exec_metrics):
            display_metric_with_target(cols[i % 2], data, metric, label)
