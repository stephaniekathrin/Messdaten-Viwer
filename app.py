import streamlit as st
import pandas as pd
from lib.data import load_csv
from lib.viz import timeseries_plot

st.set_page_config(page_title="Anlagen-Dashboard", layout="wide")

st.title("📊 Messdaten Viewer (Web-Version)")

uploaded_files = st.file_uploader("CSV-Dateien hochladen", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    df = load_csv(uploaded_files)

    st.sidebar.header("Filter")
    start = st.sidebar.date_input("Startdatum", df.index.min().date())
    end = st.sidebar.date_input("Enddatum", df.index.max().date())

    filtered = df.loc[(df.index >= pd.to_datetime(start)) & (df.index <= pd.to_datetime(end))]

    st.sidebar.header("Messwerte auswählen")
    cols = list(filtered.columns)
    primary = st.sidebar.multiselect("Primäre Achse", cols)
    secondary = st.sidebar.multiselect("Sekundäre Achse", cols)

    if not filtered.empty and (primary or secondary):
        fig = timeseries_plot(filtered, primary_cols=primary, secondary_cols=secondary)
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            label="📥 Gefilterte Daten als CSV",
            data=filtered.to_csv(sep=";").encode("utf-8"),
            file_name="gefilterte_daten.csv",
            mime="text/csv"
        )
    else:
        st.warning("Bitte Spalten auswählen.")
