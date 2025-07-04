from astm.records import PatientRecord

class ExtendedPatientRecord(PatientRecord):
    pass

# @dataclass
# class PatientRecord:
#     """ASTM Patient Record (P)"""
#     record_type: str = "P"
#     sequence_number: str = ""
#     practice_assigned_patient_id: str = ""
#     laboratory_assigned_patient_id: str = ""
#     patient_id_no_3: str = ""
#     patient_name: str = ""
#     mothers_maiden_name: str = ""
#     date_time_of_birth: Optional[str] = None
#     patient_sex: str = ""
#     patient_race_ethnic_origin: str = ""
#     patient_address: str = ""
#     reserved_field: str = ""
#     patient_telephone_number: str = ""
#     attending_physician_id: str = ""
#     special_field_1: str = ""
#     special_field_2: str = ""
#     patient_height: str = ""
#     patient_weight: str = ""
#     patients_known_diagnosis: str = ""
#     patient_active_medications: str = ""
#     patients_diet: str = ""
#     practice_field_1: str = ""
#     practice_field_2: str = ""
#     admission_and_discharge_dates: str = ""
#     admission_status: str = ""
#     location: str = ""
#     nature_of_alternative_diagnostic_code: str = ""
#     alternative_diagnostic_code: str = ""
#     patient_religion: str = ""
#     marital_status: str = ""
#     isolation_status: str = ""
#     language: str = ""
#     hospital_service: str = ""
#     hospital_institution: str = ""
#     dosage_category: str = ""
    
#     @classmethod
#     def from_record(cls, record: list) -> 'PatientRecord':
#         return cls(
#             record_type=safe_get(record, 0),
#             sequence_number=safe_get(record, 1),
#             practice_assigned_patient_id=safe_get(record, 2),
#             laboratory_assigned_patient_id=safe_get(record, 3),
#             patient_id_no_3=safe_get(record, 4),
#             patient_name=safe_get(record, 5),
#             mothers_maiden_name=safe_get(record, 6),
#             date_time_of_birth=parse_datetime(safe_get(record, 7)),
#             patient_sex=safe_get(record, 8),
#             patient_race_ethnic_origin=safe_get(record, 9),
#             patient_address=safe_get(record, 10),
#             reserved_field=safe_get(record, 11),
#             patient_telephone_number=safe_get(record, 12),
#             attending_physician_id=safe_get(record, 13),
#             special_field_1=safe_get(record, 14),
#             special_field_2=safe_get(record, 15),
#             patient_height=safe_get(record, 16),
#             patient_weight=safe_get(record, 17),
#             patients_known_diagnosis=safe_get(record, 18),
#             patient_active_medications=safe_get(record, 19),
#             patients_diet=safe_get(record, 20),
#             practice_field_1=safe_get(record, 21),
#             practice_field_2=safe_get(record, 22),
#             admission_and_discharge_dates=safe_get(record, 23),
#             admission_status=safe_get(record, 24),
#             location=safe_get(record, 25),
#             nature_of_alternative_diagnostic_code=safe_get(record, 26),
#             alternative_diagnostic_code=safe_get(record, 27),
#             patient_religion=safe_get(record, 28),
#             marital_status=safe_get(record, 29),
#             isolation_status=safe_get(record, 30),
#             language=safe_get(record, 31),
#             hospital_service=safe_get(record, 32),
#             hospital_institution=safe_get(record, 33),
#             dosage_category=safe_get(record, 34)
#         )