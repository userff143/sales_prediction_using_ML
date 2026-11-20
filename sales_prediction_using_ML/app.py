import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from src.forecasting import validate_sales, fit_and_evaluate, forecast_next_days, explain_one_prediction

st.set_page_config(page_title="Sales Prediction Using ML", page_icon="📈", layout="wide")
st.title("📈 Sales Prediction Using Machine Learning")
st.caption("Historical sales analysis • 3–7 day forecasting • Explainable AI")
DATA_PATH=Path(__file__).parent/"data"/"sample_sales_17000.csv"

with st.sidebar:
    st.header("Data settings")
    uploaded=st.file_uploader("Upload your sales CSV (optional)",type=["csv"])
    horizon=st.slider("Forecast next how many days?",3,7,7)
    st.info("Required columns: date, product_id, sales")
    st.caption("No database is used. Data is read from a CSV file in this session.")

try:
    raw=pd.read_csv(uploaded) if uploaded else pd.read_csv(DATA_PATH)
    data=validate_sales(raw)
    if uploaded:
        st.success("Your uploaded CSV is loaded for this session.")
    else:
        st.success("Bundled 17,000-row demonstration dataset loaded.")
    model,metrics,comparison,importance,data=fit_and_evaluate(data)
    forecasts=forecast_next_days(model,data,horizon)
except Exception as e:
    st.error(f"Could not prepare the data: {e}")
    st.markdown("Use a CSV with exactly these required column names: `date`, `product_id`, `sales`. Dates should be parseable and sales should be non-negative numbers.")
    st.stop()

# KPI cards
c1,c2,c3,c4=st.columns(4)
c1.metric("Historical records",f"{len(data):,}")
c2.metric("Products",f"{data.product_id.nunique():,}")
c3.metric("Test MAE",f"{metrics['MAE']:.2f}")
c4.metric("Test RMSE",f"{metrics['RMSE']:.2f}")

# Aggregate daily view
st.subheader("1. Historical sales overview")
daily=data.groupby("date",as_index=False).sales.sum()
fig=px.line(daily,x="date",y="sales",title="Total daily historical sales",labels={"date":"Date","sales":"Units sold"})
st.plotly_chart(fig,use_container_width=True)

st.subheader(f"2. Forecast for the next {horizon} days")
products=sorted(data.product_id.unique())
selected=st.selectbox("Choose a product",products)
hist=data[data.product_id==selected].copy()
fc=forecasts[forecasts.product_id==selected].copy()
plot_hist=hist.tail(45)[["date","sales"]].rename(columns={"sales":"Units"}); plot_hist["Type"]="Historical"
plot_future=fc[["date","predicted_sales"]].rename(columns={"predicted_sales":"Units"}); plot_future["Type"]="Forecast"
chart=pd.concat([plot_hist,plot_future],ignore_index=True)
fig2=px.line(chart,x="date",y="Units",color="Type",markers=True,title=f"{selected}: recent sales and future forecast")
st.plotly_chart(fig2,use_container_width=True)
st.dataframe(fc.rename(columns={"date":"Forecast date","predicted_sales":"Predicted units"}),use_container_width=True,hide_index=True)

st.subheader("3. Model evaluation")
a,b,c=st.columns(3); a.metric("MAE",f"{metrics['MAE']:.3f}"); b.metric("RMSE",f"{metrics['RMSE']:.3f}"); c.metric("R²",f"{metrics['R2']:.3f}" if pd.notna(metrics['R2']) else "Not defined")
st.caption(f"Chronological holdout: trained on {metrics['train_rows']:,} rows and tested on the latest 7 days ({metrics['test_rows']:,} rows). No random shuffling is used.")
fig3=px.scatter(comparison,x="actual_sales",y="predicted_sales",color="product_id",title="Actual vs predicted sales on the test period",labels={"actual_sales":"Actual units","predicted_sales":"Predicted units"})
fig3.add_shape(type="line",x0=0,y0=0,x1=max(comparison.actual_sales.max(),comparison.predicted_sales.max()),y1=max(comparison.actual_sales.max(),comparison.predicted_sales.max()),line=dict(dash="dash"))
st.plotly_chart(fig3,use_container_width=True)
comparison["residual"]=comparison.actual_sales-comparison.predicted_sales
fig4=px.histogram(comparison,x="residual",nbins=30,title="Forecast residual distribution",labels={"residual":"Actual − predicted units"})
st.plotly_chart(fig4,use_container_width=True)

st.subheader("4. Explainable AI – Why does the model predict this?")
st.write("Global explanation: permutation importance measures how much the model's test error worsens when a feature is shuffled. Higher values indicate greater predictive usefulness, not causation.")
fig5=px.bar(importance.sort_values("importance"),x="importance",y="feature",orientation="h",title="Global feature importance (permutation method)",labels={"importance":"Increase in prediction error","feature":"Input feature"})
st.plotly_chart(fig5,use_container_width=True)
local=explain_one_prediction(model,data,selected,horizon=1)
if not local.empty:
    st.write(f"Local sensitivity explanation for the next-day forecast of {selected}. Each bar shows how the prediction changes when one recent-sales input is increased by 10% (or weekend flag is toggled), holding other inputs fixed. This is an approximate sensitivity explanation, not a causal effect.")
    st.plotly_chart(px.bar(local.sort_values("impact"),x="impact",y="feature",orientation="h",title="Local feature sensitivity (units)",labels={"impact":"Change in prediction","feature":"Feature"}),use_container_width=True)

st.subheader("5. Download forecast results")
st.download_button("Download all product forecasts as CSV",forecasts.to_csv(index=False).encode("utf-8"),file_name="next_days_sales_forecast.csv",mime="text/csv")
st.download_button("Download model test predictions as CSV",comparison.to_csv(index=False).encode("utf-8"),file_name="model_test_predictions.csv",mime="text/csv")
with st.expander("Dataset preview and notes"):
    st.write("Bundled demo data is synthetic and intended for software testing. Replace it with a licensed real dataset for research conclusions.")
    st.dataframe(data.head(30),use_container_width=True)
    st.write("Rows:",len(data)," | Date range:",str(data.date.min().date()),"to",str(data.date.max().date()))
