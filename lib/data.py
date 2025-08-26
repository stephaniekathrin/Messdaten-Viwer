import plotly.express as px

def timeseries_plot(df, primary_cols=None, secondary_cols=None):
    """Erstellt interaktive Plotly-Grafik mit primären und sekundären Achsen."""
    if df is None or df.empty:
        return None

    fig = px.line()

    if primary_cols:
        for col in primary_cols:
            fig.add_scatter(x=df.index, y=df[col], name=col, yaxis="y1")

    if secondary_cols:
        for col in secondary_cols:
            fig.add_scatter(x=df.index, y=df[col], name=col, yaxis="y2")

    fig.update_layout(
        xaxis=dict(title="Zeit"),
        yaxis=dict(title="Primäre Achse", side="left"),
        yaxis2=dict(title="Sekundäre Achse", overlaying="y", side="right"),
        legend=dict(orientation="h")
    )
    return fig
