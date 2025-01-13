"""
Declaration of the models used by the REF.

These models are used to represent the data that is stored in the database.
"""

from typing import TypeVar

from cmip_ref.models.base import Base
from cmip_ref.models.dataset import Dataset
from cmip_ref.models.metric import Metric
from cmip_ref.models.metric_execution import MetricExecution, MetricExecutionResult
from cmip_ref.models.provider import Provider

Table = TypeVar("Table", bound=Base)


__all__ = ["Base", "Dataset", "Table", "Metric", "MetricExecution", "MetricExecutionResult", "Provider"]