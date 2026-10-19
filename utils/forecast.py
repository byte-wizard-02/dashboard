import pandas as pd
import numpy as np
import streamlit as st
from neuralprophet import NeuralProphet
from torch.serialization import safe_globals

# Allow NeuralProphet configs for PyTorch 2.6+
safe_globals(["neuralprophet.configure.ConfigSeasonality"])

@st.cache_data
def get_forecast_data(data: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Aggregate to weekly series in NeuralProphet format."""
    df = (data.groupby('Week')[metric]
                .sum()
                .reset_index()
                .rename(columns={'Week': 'ds', metric: 'y'}))
    df['ds'] = pd.to_datetime(df['ds'])
    df['y'] = pd.to_numeric(df['y'], errors='coerce').fillna(0.0)
    return df


@st.cache_resource
def train_forecast_model(df: pd.DataFrame, n_horizon: int = 8) -> NeuralProphet:
    """Train a weekly NeuralProphet model that can predict `n_horizon` steps."""
    model = NeuralProphet(
        n_changepoints=10,
        weekly_seasonality=True,
        yearly_seasonality=False,
        n_forecasts=n_horizon,
        n_lags=n_horizon,        # enable AR-Net
        epochs=100,              # raise if loss still falling
        learning_rate=0.01,
    )
    model.fit(df, freq='W')
    return model


def forecast_future(model: NeuralProphet,
                    df: pd.DataFrame,
                    periods: int = 8) -> pd.DataFrame:
    """Return forecast for `periods` future weeks."""
    future = model.make_future_dataframe(
        df,
        periods=periods,
        n_historic_predictions=len(df)   # keeps past + future in one frame
    )
    return model.predict(future)
