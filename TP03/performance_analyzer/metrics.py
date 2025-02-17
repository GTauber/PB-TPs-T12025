from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class PerformanceMetrics:
    operation: str
    time_taken: float
    elements_processed: int
    comparisons: int
    memory_used: float = 0.0 
    additional_metrics: Dict[str, Any] = None

    def __post_init__(self):
        if self.additional_metrics is None:
            self.additional_metrics = {}