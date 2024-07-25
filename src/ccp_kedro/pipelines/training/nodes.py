import ccp
import pandas as pd
import yaml
from pathlib import Path
from sklearn.cluster import KMeans
from tqdm.auto import tqdm

Q_ = ccp.Q_


def evaluate(parameters, data):
    data_units = parameters["data_units"]
    operation_fluid = parameters["operation_fluid"]
    cases = parameters["cases"]
    data_path = Path(__file__).parents[4] / "data/01_raw"
    impellers = []

    for case, case_parameters in cases.items():
        ps = Q_(case_parameters["ps"], case_parameters["ps_units"])
        Ts = Q_(case_parameters["Ts"], case_parameters["Ts_units"])
        fluid = case_parameters["fluid"]
        suc = ccp.State(p=ps, T=Ts, fluid=fluid)
        imp = ccp.Impeller.load_from_engauge_csv(
            suc=suc,
            curve_name=case,
            curve_path=data_path,
            flow_units="m³/h",
            head_units="kJ/kg",
        )
        impellers.append(imp)

    evaluation = ccp.Evaluation(
        data=data,
        operation_fluid=operation_fluid,
        data_units=data_units,
        impellers=impellers,
        n_clusters=2,
        calculate_points=False,
    )

    return evaluation
