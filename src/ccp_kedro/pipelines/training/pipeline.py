from kedro.pipeline import Pipeline, node, pipeline

from .nodes import filter_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=filter_data,
                inputs="data",
                outputs="data_filtered",
                name="filter_data_node",
            ),
        ]
    )
