from astm.records import CommentRecord

class ExtendedCommentRecord(CommentRecord):
    pass

# @dataclass
# class CommentRecord:
#     """ASTM Comment Record (C)"""
#     record_type: str = "C"
#     sequence_number: str = ""
#     comment_source: str = ""
#     comment_text: str = ""
#     comment_type: str = ""
    
#     @classmethod
#     def from_record(cls, record: list) -> 'CommentRecord':
#         return cls(
#             record_type=safe_get(record, 0),
#             sequence_number=safe_get(record, 1),
#             comment_source=safe_get(record, 2),
#             comment_text=safe_get(record, 3),
#             comment_type=safe_get(record, 4)
#         )