"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from ccp_kedro.pipelines import training as training
# from ccp_kedro.pipelines import online as online


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    training_pipeline = training.create_pipeline()
    # online_pipeline = online.create_pipeline()
    return {
        "training": training_pipeline,
        # "online": online_pipeline,
        "__default__": training_pipeline,# + online_pipeline,
    }
