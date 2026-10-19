import streamlit as st
import plotly.express as px

def render_marketing_dashboard(data):
    with st.spinner("Loading Marketing Dashboard..."):
        st.markdown("## 🟥 Marketing Metrics")

        marketing_metrics = [
            ("Website Traffic", "Website Traffic"),
            ("Social Media Engagement", "Social Media Engagement"),
            ("Campaigns Run", "Campaigns Run"),
            ("Lead Conversion", "Lead Conversion Rate"),
            ("MQLs Generated", "MQLs Generated")
        ]

        chart_type = st.selectbox(
            "📊 Choose chart type for Marketing Metrics:",
            ["Bar", "Line", "Histogram", "Pie"],
            key="marketing_chart"
        )

        for metric, label in marketing_metrics:
            st.markdown(f"**{label}**")
            grouped = data.groupby("Week")[metric].sum().reset_index()

            if chart_type == "Bar":
                fig = px.bar(grouped, x="Week", y=metric, title=label)
            elif chart_type == "Line":
                fig = px.line(grouped, x="Week", y=metric, markers=True, title=label)
            elif chart_type == "Histogram":
                fig = px.histogram(data, x=metric, title=f"Histogram of {label}")
            elif chart_type == "Pie":
                latest_week = data['Week'].max()
                pie_data = data[data['Week'] == latest_week].groupby("Region")[metric].sum().reset_index()
                fig = px.pie(pie_data, names="Region", values=metric, title=f"{label} Distribution by Region")

            st.plotly_chart(fig, use_container_width=True)

        # Download CSV
        st.download_button("⬇️ Download Marketing Data as CSV", data.to_csv(index=False), file_name="marketing_data.csv")
        st.info("🔗 This is demo data. Real-time marketing data can be integrated in future.")
