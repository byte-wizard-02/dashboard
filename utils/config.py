import streamlit as st

def apply_styles():
    with open("assets/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Default KPI Targets
def get_default_targets():
    return {
        'New Leads': 40,
        'Deals Closed': 15,
        'Revenue Closed': 7000,
        'New Hires': 5,
        'Website Traffic': 5000,
        'Strategic Projects': 2
    }

# Let Admin update KPI targets in sidebar
def update_kpi_targets(role):
    if 'targets' not in st.session_state:
        st.session_state.targets = get_default_targets()

    if role == "Admin":
        st.sidebar.markdown("### 🎯 Edit KPI Targets")
        for metric in st.session_state.targets:
            new_val = st.sidebar.number_input(
                f"Target - {metric}",
                value=int(st.session_state.targets[metric]),
                step=1
            )
            st.session_state.targets[metric] = new_val
