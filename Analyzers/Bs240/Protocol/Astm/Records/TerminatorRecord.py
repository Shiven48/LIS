from dataclasses import dataclass
from utility import safe_get

@dataclass
class TerminatorRecord:
    """ASTM Terminator Record (L)"""
    record_type: str = "L"
    sequence_number: str = ""
    termination_code: str = ""
    
    @classmethod
    def from_record(cls, record: list) -> 'TerminatorRecord':
        return cls(
            record_type=safe_get(record, 0),
            sequence_number=safe_get(record, 1),
            termination_code=safe_get(record, 2)
        )