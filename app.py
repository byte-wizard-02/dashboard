import streamlit as st
import pandas as pd

from utils.auth import get_user_role_and_section
from utils.config import apply_styles, update_kpi_targets
from utils.data_loader import load_main_data
from sections.sales import render_sales_dashboard
from sections.hr import render_hr_dashboard
from sections.marketing import render_marketing_dashboard
from sections.executive import render_executive_dashboard
from sections.summary import render_summary_charts
from sections.developer import render_developer_dashboard # If Developer section added

# --- Setup page ---
st.set_page_config(page_title="Samfield Capital Dashboard", layout="wide")
apply_styles()

# --- Authentication & Navigation ---
role, section = get_user_role_and_section()

# --- Load raw data ---
data = load_main_data()

# --- Admin-only sidebar controls ---
if role == "Admin":
    st.sidebar.markdown("### 🧭 Data Filters")
    # Filter by Region
    regions = sorted(data["Region"].unique())
    selected_regions = st.sidebar.multiselect("Select Region(s)", regions, default=regions)
    # Filter by Date Range
    min_date = data["Week"].min().date()
    max_date = data["Week"].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    # Ensure date_range is tuple/list of two dates
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    else:
        # fallback if single date selected
        start_date = end_date = pd.to_datetime(date_range)
    # Apply filters to data
    data = data[
        (data["Region"].isin(selected_regions)) &
        (data["Week"] >= start_date) &
        (data["Week"] <= end_date)
    ]
    # Saved Views (pre-set filters for example)
    st.sidebar.markdown("### 📁 Saved Views")
    saved_view = st.sidebar.selectbox("Load a Saved View", ["None", "West Only", "Q2 Only"])
    if saved_view == "West Only":
        data = data[data["Region"] == "West"]
    elif saved_view == "Q2 Only":
        data = data[data["Week"].dt.quarter == 2]
    # KPI Targets editing
    update_kpi_targets(role)

# --- Dashboard Rendering ---
if section == "Sales" and role in ["Admin", "Sales"]:
    render_sales_dashboard(data, role) # Pass role for admin-only commission etc.
elif section == "HR" and role in ["Admin", "HR"]:
    render_hr_dashboard(data)
elif section == "Marketing" and role in ["Admin", "Marketing"]:
    render_marketing_dashboard(data)
elif section == "Executive Office" and role in ["Admin", "Executive Office"]:
    render_executive_dashboard(data)
elif section == "Developer" and role in ["Admin", "Developer"]:
    render_developer_dashboard(data)
else:
    st.warning("🚫 You do not have access to this section.")

# --- Shared Summary Charts ---
render_summary_charts(data, role)
