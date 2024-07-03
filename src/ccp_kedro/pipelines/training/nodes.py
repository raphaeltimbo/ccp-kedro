import ccp
import pandas as pd
import yaml
from pathlib import Path
from sklearn.cluster import KMeans

Q_ = ccp.Q_


def filter_data(
    data,
    data_type={
        "ps": "pressure",
        "Ts": "temperature",
        "pd": "pressure",
        "Td": "temperature",
        "speed": "speed",
    },
):
    return ccp.data_io.filter_data(data, data_type=data_type)


def calculate_flow(data_filtered, parameters):
    # from parameters
    data_units = parameters["data_units"]
    operation_fluid = parameters["operation_fluid"]
    # create density column
    df = data_filtered
    df["v_s"] = 0
    df["speed_sound"] = 0
    for i, row in df.iterrows():
        # create state
        state = ccp.State(
            p=Q_(row.ps, data_units["ps"]),
            T=Q_(row.Ts, data_units["Ts"]),
            fluid=operation_fluid,
        )
        df.loc[i, "v_s"] = state.v().m
        df.loc[i, "speed_sound"] = state.speed_sound().m

    # check if flow_v or flow_m is in the DataFrame
    if "flow_v" in df.columns:
        # create flow_m column
        df["flow_m"] = (
            Q_(df["flow_v"].array, data_units["flow_v"]) * Q_(df["v_s"].array, "m³/kg")
        ).m
    elif "flow_m" in df.columns:
        # create flow_v column
        df["flow_v"] = (
            Q_(df["flow_m"].array, data_units["flow_m"]) / Q_(df["v_s"].array, "m³/kg")
        ).m
    else:
        raise ValueError("Flow rate not found in the DataFrame.")

    return df
