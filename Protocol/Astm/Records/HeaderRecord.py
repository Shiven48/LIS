from astm.records import HeaderRecord
from astm.mapping import TextField


class ExtendedHeader(HeaderRecord):
    sender = TextField(name="sender", length=50)

class ExtraHeaderFields(ExtendedHeader):
    vowels = TextField(name="vowels", length=5)


# @dataclass
# class HeaderRecord:

#     record_type: str = "H"
#     delimiter_definition: str = ""
#     message_control_id: str = ""
#     access_password: Optional[str] = None
#     sender_name_id: Optional[str] = None
#     sender_reserved_field: Optional[str] = None
#     sender_telephone: Optional[str] = None
#     date_time_of_message: Optional[str] = None

#     @classmethod
#     def from_record(cls, record: list) -> 'HeaderRecord':
#         return cls(
#             record_type=safe_get(record, 0),
#             delimiter_definition=safe_get(record, 1),
#             message_control_id=safe_get(record, 2),
#             access_password=safe_get(record, 3),
#             sender_name_id=safe_get(record, 4),
#             sender_reserved_field=safe_get(record, 6),
#             sender_telephone=safe_get(record, 7),
#             date_time_of_message=parse_datetime(safe_get(record, 8)),
#         )