"""
Rapid evaluating CMIP data
"""

import importlib.metadata

from ref_core.providers import MetricsProvider

from ref_metrics_example.example import GlobalMeanTimeseries

__version__ = importlib.metadata.version("ref_metrics_example")
__core_version__ = importlib.metadata.version("ref_core")

# Initialise the metrics manager and register the example metric
provider = MetricsProvider("Example", __version__)
provider.register(GlobalMeanTimeseries())
