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
    tappings = parameters["tappings"]
    D = Q_(parameters["D"], data_units["D"])
    d = Q_(parameters["d"], data_units["d"])
    state = ccp.State(
        p=Q_(data_filtered["ps"].iloc[0], data_units["ps"]),
        T=Q_(data_filtered["Ts"].iloc[0], data_units["Ts"]),
        fluid=operation_fluid,
    )
    # create density column
    df = data_filtered
    df["v_s"] = 0
    df["speed_sound"] = 0
    # check if flow_v or flow_m are in the DataFrame
    calculate_flow_from_delta_p = False
    if not ("flow_v" in df.columns or "flow_m" in df.columns):
        calculate_flow_from_delta_p = True
        df["flow_v"] = 0
        df["flow_m"] = 0

    for i, row in df.iterrows():
        # update state
        ps = Q_(row.ps, data_units["ps"])
        Ts = Q_(row.Ts, data_units["Ts"])
        state.update(p=ps, T=Ts, fluid=operation_fluid)
        df.loc[i, "v_s"] = state.v().m
        df.loc[i, "speed_sound"] = state.speed_sound().m

        if calculate_flow_from_delta_p:
            delta_p = Q_(row.delta_p, data_units["delta_p"])
            fo = ccp.FlowOrifice(
                state=state,
                delta_p=delta_p,
                D=D,
                d=d,
                tappings=tappings,
            )
            df.loc[i, "flow_v"] = fo.flow_v.m
            df.loc[i, "flow_m"] = fo.flow_m.m

    if not calculate_flow_from_delta_p:
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


def create_clusters(data_with_flow):
    df = data_with_flow
    # create clusters based on speed_sound, ps and Ts
    data = df[["speed_sound", "ps", "Ts"]]
    # normalize
    data_mean = data.mean()
    data_std = data.std()
    data_norm = (data - data_mean) / data_std

    # Using sklearn
    kmeans = KMeans(n_clusters=5, n_init="auto")
    kmeans.fit(data_norm)

    # Format results as a DataFrame
    df["cluster"] = kmeans.labels_
    for i in range(kmeans.n_clusters):
        df.loc[df["cluster"] == i, "speed_sound_center"] = (
            kmeans.cluster_centers_[i][0] * data_std["speed_sound"]
        ) + data_mean["speed_sound"]
        df.loc[df["cluster"] == i, "ps_center"] = (
            kmeans.cluster_centers_[i][1] * data_std["ps"]
        ) + data_mean["ps"]
        df.loc[df["cluster"] == i, "Ts_center"] = (
            kmeans.cluster_centers_[i][0] * data_std["Ts"]
        ) + data_mean["Ts"]

    return df


def create_impellers(parameters):
    pass
