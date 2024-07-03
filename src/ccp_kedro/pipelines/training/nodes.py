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

