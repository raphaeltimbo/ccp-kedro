from kedro.pipeline import Pipeline, node, pipeline

from .nodes import filter_data, calculate_flow, create_clusters


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=filter_data,
                inputs="data",
                outputs="data_filtered",
                name="filter_data_node",
            ),
            node(
                func=calculate_flow,
                inputs=["data_filtered", "parameters"],
                outputs="data_with_flow",
                name="calculate_flow_node",
            ),
            node(
                func=create_clusters,
                inputs=["data_with_flow", "parameters"],
                outputs="impellers_new",
                name="create_clusters_node",
            ),
        ]
    )
