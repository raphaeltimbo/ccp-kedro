from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import evaluate

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=evaluate,
                inputs=["parameters", "data"],
                outputs="evaluation",
                name="evaluate_node",
            ),
        ]
    )
