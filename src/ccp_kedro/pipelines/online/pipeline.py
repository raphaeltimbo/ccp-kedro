from kedro.pipeline import Pipeline, node, pipeline

from .nodes import calculate_points


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=calculate_points,
                inputs=["data_online", "impellers"],
                outputs="data_calculated",
                name="calculate_points_node",
            ),
        ]
    )
