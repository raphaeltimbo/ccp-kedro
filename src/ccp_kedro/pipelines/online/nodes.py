import ccp
import numpy as np


def calculate_points(parameters, data_online, impellers_new):
    data_units = parameters["data_units"]
    operation_fluid = parameters["operation_fluid"]
    suc = ccp.State(
        p=Q_(data_online["ps"].iloc[0], data_units["ps"]),
        T=Q_(data_online["Ts"].iloc[0], data_units["Ts"]),
        fluid=operation_fluid,
    )

    speed_sound_diff = []
    for impeller in impellers_new:
        speed_sound_diff.append(
            impeller.points[0].suc.speed_sound() - suc.sound_speed()
        )
    imp = impellers_new[np.argmin(np.abs(speed_sound_diff))]
    pass
