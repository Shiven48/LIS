from astm.records import ResultRecord

class ExtendedResultRecord(ResultRecord):
    pass

# from dataclasses import dataclass
# from typing import Optional

# @dataclass
# class ResultRecord:
#     record_type: str       
#     sequence_number: str   
#     test_id: str           
#     value: Optional[str] = None
#     units: Optional[str] = None
#     reference_range: Optional[str] = None
#     abnormal_flag: Optional[str] = None  
#     result_status: Optional[str] = None  

#     @classmethod
#     def from_record(cls, rec: list) -> "ResultRecord":
#         return cls(
#             record_type=rec[0],
#             sequence_number=rec[1],
#             test_id="|".join(rec[2]) if isinstance(rec[2], (list, tuple)) else rec[2],
#             value=safe_get(rec, 3),
#             units=safe_get(rec, 4),
#             reference_range=safe_get(rec, 5),
#             abnormal_flag=safe_get(rec, 6),
#             result_status=safe_get(rec, 10)
#         )
