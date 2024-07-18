from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import calculate_points

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=calculate_points,
                inputs=["parameters", "data_online", "impellers_new"],
                outputs="data_calculated",
                name="calculate_points_node",
            ),
        ]
    )
