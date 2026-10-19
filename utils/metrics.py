import streamlit as st

def display_metric_with_target(col, data, metric, label):
    current = data[metric].iloc[-1]
    previous = data[metric].iloc[-2] if len(data) > 1 else current
    change = current - previous

    # Alert icons
    alert = ""
    if previous and previous != 0:
        ratio = change / previous
        if ratio > 0.25:
            alert = "📍 Spike"
        elif ratio < -0.25:
            alert = "⚠️ Drop"

    # Get KPI target from session
    target = st.session_state.get("targets", {}).get(metric)

    # Show metric label with full wrapping
    col.markdown(
        f"""
        <div style='font-weight:600; font-size:14px; margin-bottom: 0.2rem; white-space: normal; line-height: 1.3em;'>
            {label} {alert}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render value and delta
    if target is not None:
        delta = float(current - target)
        col.metric(label="", value=f"{int(current)} / {target}", delta=delta)
    else:
        col.metric(label="", value=int(current))
