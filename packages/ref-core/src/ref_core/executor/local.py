from ref_core.metrics import Metric, MetricExecutionDefinition, MetricResult


class LocalExecutor:
    """
    Run a metric locally, in-process.

    This is mainly useful for debugging and testing.
    The production executor will run the metric in a separate process or container,
    the exact manner of which is yet to be determined.
    """

    name = "local"

    def run_metric(self, metric: Metric, definition: MetricExecutionDefinition) -> MetricResult:
        """
        Run a metric in process

        Parameters
        ----------
        metric
            Metric to run
        definition
            Information about the execution of the metric
        trigger
            Information about the dataset that triggered the metric run
        kwargs
            Additional keyword arguments for the executor

        Returns
        -------
        :
            Results from running the metric
        """
        return metric.run(definition=definition)
