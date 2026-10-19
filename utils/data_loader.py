import os
import pandas as pd
import numpy as np
import streamlit as st
import requests
from datetime import datetime, timedelta

@st.cache_data
def load_hr_data():
    url = "https://api.sensehr.io/employees"  # Placeholder
    headers = {"Authorization": "Bearer YOUR_API_KEY"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e:
        st.warning(f"⚠️ Could not load HR API data: {e}")

        # Fallback 1: local CSV
        if os.path.exists("mock_sensehr_data.csv"):
            st.info("📄 Using local mock HR data.")
            return pd.read_csv("mock_sensehr_data.csv", parse_dates=["Joining Date", "Hire Date", "Application Date"])

        # Fallback 2: dummy data
        st.info("📦 Using built-in dummy HR data.")
        return pd.DataFrame({
            "Employee Name": ["Alice", "Bob", "Charlie", "Diana"],
            "Department": ["HR"] * 4,
            "Joining Date": pd.date_range(start="2023-01-01", periods=4, freq="3M"),
            "Status": ["Active", "Active", "On Leave", "Resigned"],
            "Engagement Score": [78, 82, 75, 80],
            "Training Effectiveness": [76, 80, 79, 77],
            "Performance Rating": [85, 90, 80, 78],
            "Hiring Cost": [4000, 5000, 6000, 5500],
            "Internal Moves": [1, 0, 0, 1],
            "Overtime Hours": [10, 5, 12, 0],
            "Application Status": ["Accepted", "Offered", "Accepted", "Rejected"],
            "Gender": ["Female", "Male", "Female", "Male"],
            "Application Date": pd.date_range("2022-11-01", periods=4, freq="2M"),
            "Hire Date": pd.date_range("2023-01-01", periods=4, freq="2M")
        })

@st.cache_data
def load_main_data():
    np.random.seed(42)
    dates = pd.date_range(end=datetime.today(), periods=24, freq='W')
    regions = ['North', 'South', 'East', 'West']
    return pd.DataFrame({
        'Week': np.tile(dates, len(regions)),
        'Region': np.repeat(regions, len(dates)),
        'New Leads': np.random.randint(20, 50, size=96),
        'Meetings Booked': np.random.randint(10, 30, size=96),
        'Discovery Calls': np.random.randint(5, 20, size=96),
        'Proposals Sent': np.random.randint(5, 15, size=96),
        'Follow-ups': np.random.randint(10, 25, size=96),
        'Referrals': np.random.randint(2, 10, size=96),
        'CRM Activity': np.random.randint(50, 100, size=96),
        'Content Engagement': np.random.randint(30, 80, size=96),
        'Deals Closed': np.random.randint(5, 20, size=96),
        'Revenue Closed': np.random.randint(1000, 10000, size=96),
        'Sales Cycle Length': np.random.uniform(5, 20, size=96),
        'Conversion Rate': np.random.uniform(0.1, 0.5, size=96),
        'Client Acquisition Cost': np.random.randint(100, 1000, size=96),
        'Forecasted Revenue': np.random.randint(5000, 15000, size=96),
        'New Hires': np.random.randint(0, 10, size=96),
        'Interviews Conducted': np.random.randint(5, 20, size=96),
        'Employee Turnover': np.random.randint(0, 5, size=96),
        'Engagement Score': np.random.uniform(60, 90, size=96),
        'Training Hours': np.random.randint(10, 50, size=96),
        'Job Applications': np.random.randint(50, 150, size=96),
        'Website Traffic': np.random.randint(1000, 10000, size=96),
        'Social Media Engagement': np.random.randint(200, 1000, size=96),
        'Campaigns Run': np.random.randint(1, 5, size=96),
        'Lead Conversion': np.random.uniform(0.1, 0.6, size=96),
        'MQLs Generated': np.random.randint(10, 100, size=96),
        'Strategic Projects': np.random.randint(1, 3, size=96),
        'Weekly Objectives Met': np.random.randint(2, 5, size=96),
        'Cross-team Meetings': np.random.randint(3, 10, size=96),
        'Compliance Score': np.random.uniform(85, 100, size=96)
    })
