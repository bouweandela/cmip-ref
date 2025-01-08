"""
Rapid evaluating CMIP data with ESMValTool.
"""

from ref_core.providers import MetricsProvider

from ref_metrics_esmvaltool._version import __version__
from ref_metrics_esmvaltool.ecs import EquilibriumClimateSensitivity
from ref_metrics_esmvaltool.example import GlobalMeanTimeseries

# Initialise the metrics manager and register the example metric
provider = MetricsProvider("ESMValTool", __version__)
provider.register(GlobalMeanTimeseries())
provider.register(EquilibriumClimateSensitivity())
