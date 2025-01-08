from typing import Any

import xarray
from ref_core.datasets import FacetFilter, SourceDatasetType
from ref_core.metrics import DataRequirement, Metric, MetricExecutionDefinition, MetricResult
from ruamel.yaml import YAML

from ref_metrics_esmvaltool._version import __version__
from ref_metrics_esmvaltool.recipe import dataframe_to_recipe, load_recipe, run_recipe

yaml = YAML()


def format_cmec_output_bundle(dataset: xarray.Dataset) -> dict[str, Any]:
    """
    Create a simple CMEC output bundle for the dataset.

    Parameters
    ----------
    dataset
        Processed dataset

    Returns
    -------
        A CMEC output bundle ready to be written to disk
    """
    source_id = dataset.dataset.values[0].decode("utf-8")
    cmec_output = {
        "DIMENSIONS": {
            "dimensions": {
                "source_id": {source_id: {}},
                "region": {"global": {}},
                "variable": {"ecs": {}},
            },
            "json_structure": [
                "model",
                "region",
                "statistic",
            ],
        },
        # Is the schema tracked?
        "SCHEMA": {
            "name": "CMEC-REF",
            "package": "ref_metrics_esmvaltool",
            "version": __version__,
        },
        "RESULTS": {
            source_id: {"global": {"ecs": dataset.ecs.values[0]}},
        },
    }

    return cmec_output


class EquilibriumClimateSensitivity(Metric):
    """
    Calculate the global mean equilibrium climate sensitivity for a dataset.
    """

    name = "Equilibrium Climate Sensitivity"
    slug = "esmvaltool-equilibrium-climate-sensitivity"

    data_requirements = (
        DataRequirement(
            source_type=SourceDatasetType.CMIP6,
            filters=(
                FacetFilter(
                    facets={
                        "variable_id": (
                            "rlut",
                            "rsdt",
                            "rsut",
                            "tas",
                        ),
                        "experiment_id": (
                            "abrupt-4xCO2",
                            "piControl",
                        ),
                    },
                ),
            ),
            # TODO: Select only datasets that have both experiments and all four variables
            # TODO: Select only datasets that have a contiguous, shared timerange
            # TODO: Add cell areas to the groups
            # constraints=(AddCellAreas(),),
            group_by=("source_id", "variant_label"),
        ),
    )

    def run(self, definition: MetricExecutionDefinition) -> MetricResult:
        """
        Run a metric

        Parameters
        ----------
        definition
            A description of the information needed for this execution of the metric

        Returns
        -------
        :
            The result of running the metric.
        """
        recipe = load_recipe("recipe_ecs.yml")

        # Only run the diagnostic that computes ECS for a single model.
        recipe["diagnostics"] = {
            "cmip6": {
                "description": "Calculate ECS.",
                "variables": {
                    "tas": {
                        "preprocessor": "spatial_mean",
                    },
                    "rtnt": {
                        "preprocessor": "spatial_mean",
                        "derive": True,
                    },
                },
                "scripts": {
                    "ecs": {
                        "script": "climate_metrics/ecs.py",
                        "calculate_mmm": False,
                    },
                },
            },
        }

        # Prepare updated datasets section in recipe. It contains two
        # datasets, one for the "abrupt-4xCO2" and one for the "piControl"
        # experiment.
        recipe_variables = dataframe_to_recipe(definition.metric_dataset[SourceDatasetType.CMIP6].datasets)

        # Select a timerange covered by all datasets. Maybe this should be done
        # when selecting input data already.
        start_times, end_times = [], []
        for variable in recipe_variables.values():
            for dataset in variable["additional_datasets"]:
                start, end = dataset["timerange"].split("/")
                start_times.append(start)
                end_times.append(end)
        timerange = f"{max(start_times)}/{min(end_times)}"

        datasets = recipe_variables["tas"]["additional_datasets"]
        for dataset in datasets:
            dataset["timerange"] = timerange

        recipe["datasets"] = datasets

        # Run recipe
        result_dir = run_recipe(recipe, definition)
        result = next(result_dir.glob("work/cmip6/ecs/ecs.nc"))
        ecs = xarray.open_dataset(result)

        return MetricResult.build_from_output_bundle(definition, format_cmec_output_bundle(ecs))
