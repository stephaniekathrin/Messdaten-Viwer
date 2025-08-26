import pandas as pd

def apply_damping_by_index(df, col_index, damp_s=3.0, dt=0.1, suffix="_damped"):
    df = df.copy()
    col_in = df.columns[col_index]
    col_out = f"{col_in}{suffix}"

    if not pd.api.types.is_numeric_dtype(df[col_in]):
        raise ValueError(f"Spalte {col_in} ist nicht numerisch und kann nicht gedämpft werden.")

    values = df[col_in].values
    PV = [values[0]]
    for i in range(1, len(values)):
        diff = values[i] - PV[-1]
        PV_new = (diff / damp_s) * dt + PV[-1]
        PV.append(PV_new)
    df[col_out] = PV
    return df


def load_csv(files):
    """Liest CSV-Dateien wie in deiner Desktop-App und fügt sie zusammen."""
    all_data = []
    titles, units = None, None

    for file in files:
        raw = pd.read_csv(file, sep=";", header=None, encoding="latin1")
        titles = [x.replace("'", "") for x in list(raw.iloc[1])]
        units = [x.replace("'", "") for x in list(raw.iloc[2])]
        titles[0] = "Date"; titles[1] = "Time"

        data = raw.iloc[3:].reset_index(drop=True)
        data.columns = titles
        data["Datetime"] = pd.to_datetime(
            data[titles[0]] + " " + data[titles[1]], dayfirst=True, errors="coerce"
        )
        data = data.drop(columns=[titles[0], titles[1]])
        data = data.set_index("Datetime")
        data = data.apply(lambda col: col.astype(str).str.replace(",", ".", regex=False))
        data = data.apply(pd.to_numeric, errors="coerce")

        # Zusätzliche Spalten berechnen
        if "Solid circulation rate" in data.columns:
            damped_df = apply_damping_by_index(
                data, data.columns.get_loc("Solid circulation rate"),
                damp_s=40, dt=1, suffix="_damped"
            )
            data["SCR-PD"] = (damped_df["Solid circulation rate_damped"] ** 1.576) * 16.813

        if "Press. meas. monit. solid stream flow" in data.columns:
            data["SCR-LR"] = (data["Press. meas. monit. solid stream flow"] ** 1.576) * 16.813

        all_data.append(data)

    return pd.concat(all_data).sort_index()

