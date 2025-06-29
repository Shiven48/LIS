from astm.records import OrderRecord

class ExtendedOrderRecord(OrderRecord):
    pass

# @dataclass
# class OrderRecord:
#     """ASTM Order Record (O)"""
#     record_type: str = "O"
#     sequence_number: str = ""
#     specimen_id: str = ""
#     instrument_specimen_id: str = ""
#     universal_test_id: str = ""
#     priority: str = ""
#     requested_ordered_date_time: Optional[str] = None
#     specimen_collection_date_time: Optional[str] = None
#     collection_end_time: Optional[str] = None
#     collection_volume: str = ""
#     collector_id: str = ""
#     action_code: str = ""
#     danger_code: str = ""
#     relevant_clinical_information: str = ""
#     date_time_specimen_received: Optional[str] = None
#     specimen_descriptor: str = ""
#     ordering_physician: str = ""
#     physicians_telephone_number: str = ""
#     user_field_1: str = ""
#     user_field_2: str = ""
#     laboratory_field_1: str = ""
#     laboratory_field_2: str = ""
#     date_time_results_reported: Optional[str] = None
#     instrument_charge_to_computer_system: str = ""
#     instrument_section_id: str = ""
#     report_types: str = ""
#     reserved_field: str = ""
#     location_ward_of_specimen_collection: str = ""
#     nosocomial_infection_flag: str = ""
#     specimen_service: str = ""
#     specimen_institution: str = ""
    
#     @classmethod
#     def from_record(cls, record: list) -> 'OrderRecord':
#         return cls(
#             record_type=safe_get(record, 0),
#             sequence_number=safe_get(record, 1),
#             specimen_id=safe_get(record, 2),
#             instrument_specimen_id=safe_get(record, 3),
#             universal_test_id=safe_get(record, 4),
#             priority=safe_get(record, 5),
#             requested_ordered_date_time=parse_datetime(safe_get(record, 6)),
#             specimen_collection_date_time=parse_datetime(safe_get(record, 7)),
#             collection_end_time=parse_datetime(safe_get(record, 8)),
#             collection_volume=safe_get(record, 9),
#             collector_id=safe_get(record, 10),
#             action_code=safe_get(record, 11),
#             danger_code=safe_get(record, 12),
#             relevant_clinical_information=safe_get(record, 13),
#             date_time_specimen_received=parse_datetime(safe_get(record, 14)),
#             specimen_descriptor=safe_get(record, 15),
#             ordering_physician=safe_get(record, 16),
#             physicians_telephone_number=safe_get(record, 17),
#             user_field_1=safe_get(record, 18),
#             user_field_2=safe_get(record, 19),
#             laboratory_field_1=safe_get(record, 20),
#             laboratory_field_2=safe_get(record, 21),
#             date_time_results_reported=parse_datetime(safe_get(record, 22)),
#             instrument_charge_to_computer_system=safe_get(record, 23),
#             instrument_section_id=safe_get(record, 24),
#             report_types=safe_get(record, 25),
#             reserved_field=safe_get(record, 26),
#             location_ward_of_specimen_collection=safe_get(record, 27),
#             nosocomial_infection_flag=safe_get(record, 28),
#             specimen_service=safe_get(record, 29),
#             specimen_institution=safe_get(record, 30)
#         )