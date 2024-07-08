from kedro.pipeline import Pipeline, node, pipeline

from .nodes import filter_data, calculate_flow, create_clusters, create_impellers


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
                inputs="data_with_flow",
                outputs="data_with_clusters",
                name="create_clusters_node",
            ),
            node(
                func=create_impellers,
                inputs=["parameters"],
                outputs="impellers",
                name="create_impellers_node",
            )
            # convert curves
            # save impellers
        ]
    )
