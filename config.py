ASTM_END_BLOCK = b'\x17'
HL7_START_BLOCK = b'\x0B'
HL7_END_BLOCK = b'\x1C\r'

# For Serial Setup
DEFAULT_SERIAL_PORT = "COM3"
DEFAULT_BAUD_RATE = "9600"
DEFAULT_DATA_BITS = "8"
DEFAULT_PARITY = "NONE"
DEFAULT_STOP_BITS = "1"

# For log file
LOG_FILE_PATH = "logs/app.log"
MAX_FRAME_BODY_SIZE = 240

single_test = ('1H|\\^&|BS240|MINDRAY|Mindray BS-240|123 Healthcare Ave^^Mumbai^MH^400001|Lab Manager|+919876543210|CAPS-A|LabSystem|Clinical Chemistry|P|1.2.1|20250626140530|\r'
    'P|1|12345||67890|SHARMA^RAJESH^KUMAR|PATEL|19850315|M|I|402 Tower A^^Mumbai^MH^400052||+919988776655|DR001|INS12345|POL67890|178|72|HTN^DM|Amlodipine^Metformin|Vegetarian^Diabetic|CARDIO|REF001|20250625^20250627|Outpatient|General Ward\r'
    'O|1|GLU01||^^^GLU^Glucose||20250626080000|||||F||||1||||||||||O\r'
    'R|1|^^^GLU^Glucose|125.5|mg/dL|70_99|H||F||tech001|20250626081500||V1.0|MINDRAY BS-240\r'
    'O|2|CHOL01||^^^CHOL^Total Cholesterol||20250626080100|||||F||||1||||||||||O\r'
    'R|2|^^^CHOL^Total Cholesterol|185.2|mg/dL|<200|N||F||tech001|20250626081600||V1.0|MINDRAY BS-240\r'
    'C|1|I|Patient fasting for 12 hours|G\r'
    'L|1|N')