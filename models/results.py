from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TestResult:
    test_type: str
    status: str
    rating: str | None
    attempts: int | None
    elapsed_seconds: float
    timestamp: datetime