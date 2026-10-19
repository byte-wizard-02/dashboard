import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.forecast import get_forecast_data, train_forecast_model, forecast_future
from utils.config import update_kpi_targets

def render_summary_charts(data, role):
    st.markdown("## 📝 Executive Summary")

    # --- Show summary changes ---
    summaries = []
    for metric in ["Revenue Closed", "New Leads", "Deals Closed"]:
        if len(data) > 1:
            prev_value = data[metric].iloc[-2]
            diff = data[metric].iloc[-1] - prev_value
            pct = round((diff / prev_value) * 100, 1) if prev_value else 0
            direction = "increased" if diff > 0 else "decreased"
            summaries.append(f"{metric} {direction} by {abs(pct)}% compared to last week.")
    for line in summaries:
        st.write(f"- {line}")

    # --- Regional Chart ---
    st.subheader("📊 Regional Metric Chart")
    chart_type_region = st.selectbox(
        "Chart type for regional breakdown:",
        ["Bar Chart", "Line Chart", "Area Chart", "Histogram", "Pie Chart"],
        key="region_chart_type"
    )
    selected_metric_region = st.selectbox(
        "Metric to display by region:",
        ["Revenue Closed", "New Leads", "Deals Closed"],
        key="region_metric"
    )

    agg_data_region = data.groupby(["Region", "Week"])[selected_metric_region].sum().reset_index()

    if chart_type_region == "Bar Chart":
        agg_sum_region = agg_data_region.groupby("Region")[selected_metric_region].sum().reset_index()
        fig = px.bar(agg_sum_region, x='Region', y=selected_metric_region, color='Region')
    elif chart_type_region == "Line Chart":
        fig = px.line(agg_data_region, x='Week', y=selected_metric_region, color='Region', markers=True)
    elif chart_type_region == "Area Chart":
        fig = px.area(agg_data_region, x='Week', y=selected_metric_region, color='Region')
    elif chart_type_region == "Histogram":
        fig = px.histogram(data, x=selected_metric_region, color='Region', barmode='overlay')
    elif chart_type_region == "Pie Chart":
        pie_data = agg_data_region.groupby("Region")[selected_metric_region].sum().reset_index()
        fig = px.pie(pie_data, names="Region", values=selected_metric_region)

    st.plotly_chart(fig, use_container_width=True)

    # --- Multi-Metric Comparison ---
    st.subheader("📊 Multi-Metric Comparison")
    chart_type_multi = st.selectbox(
        "Chart type for multi-metric comparison:",
        ["Bar Chart", "Line Chart", "Area Chart", "Histogram", "Pie Chart"],
        key="multi_chart_type"
    )

    selected_metrics_multi = st.multiselect(
        "Select metrics to compare:",
        options=list(data.columns[2:]),
        default=["New Leads", "Deals Closed"],
        key="multi_metrics"
    )

    if selected_metrics_multi:
        if chart_type_multi == "Bar Chart":
            agg_data_multi = data.groupby("Region")[selected_metrics_multi].sum().reset_index()
            fig = go.Figure()
            for metric in selected_metrics_multi:
                fig.add_trace(go.Bar(x=agg_data_multi["Region"], y=agg_data_multi[metric], name=metric))
            fig.update_layout(barmode='group')
        elif chart_type_multi == "Line Chart":
            fig = px.line(data, x='Week', y=selected_metrics_multi, color='Region', markers=True)
        elif chart_type_multi == "Area Chart":
            fig = px.area(data, x='Week', y=selected_metrics_multi[0], color='Region')
        elif chart_type_multi == "Histogram":
            fig = px.histogram(data, x=selected_metrics_multi[0], color='Region', barmode='overlay')
        elif chart_type_multi == "Pie Chart":
            pie_data = data.groupby("Region")[selected_metrics_multi[0]].sum().reset_index()
            fig = px.pie(pie_data, names='Region', values=selected_metrics_multi[0])
        st.plotly_chart(fig, use_container_width=True)

    # --- Forecasting Section ---
    st.subheader("🔮 Forecasting & Predictive Analytics")
    st.write("📈 Predict future performance trends with NeuralProphet.")

    forecast_metric = st.selectbox(
        "Metric to forecast:",
        ["Revenue Closed", "New Leads", "Deals Closed", "DEBUG"],
        key="forecast_metric"
    )
    chart_type_forecast = st.radio("Forecast chart type:", ["Line Chart", "Bar Chart"], key="forecast_chart")

    if forecast_metric == "DEBUG":
        forecast_data = get_forecast_data(data, "Revenue Closed")
        forecast_data["y"] = 1000 + (forecast_data.index * 250) + (50 * st.session_state.get("forecast_variance", 1))
    else:
        forecast_data = get_forecast_data(data, forecast_metric)

    if forecast_data.empty or 'y' not in forecast_data.columns or forecast_data['y'].sum() == 0:
        st.warning(f"⚠️ No data available for forecasting '{forecast_metric}'. Try DEBUG mode or adjust filters.")
        return

    try:
        model = train_forecast_model(forecast_data)
        forecast = forecast_future(model, forecast_data, periods=8)

        if chart_type_forecast == "Line Chart":
            fig_forecast = px.line(forecast, x='ds', y='yhat1', title=f"{forecast_metric} Forecast")
            fig_forecast.add_scatter(x=forecast_data['ds'], y=forecast_data['y'], mode='markers', name='Actual')
            st.plotly_chart(fig_forecast, use_container_width=True)
        else:
            fig_bar = px.bar(forecast, x='ds', y='yhat1', title=f"{forecast_metric} Forecast")
            st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Forecasting failed: {e}")
        import traceback
        st.code(traceback.format_exc())

    # --- Notes & Downloads ---
    if role == "Admin":
        st.subheader("🗨️ Notes & Context")
        notes = st.text_area("Add notes for this week's data:")
        if notes:
            st.success("Note saved (in memory)")

    st.subheader("⬇️ Download Data")
    st.download_button("Download CSV", data.to_csv(index=False), file_name="dashboard_data.csv")
