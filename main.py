from Analyzers.Bs240.Protocol.Astm.Parser.Astmparser import enhanced_decode, frame_astm_message
from Analyzers.Bs240.Protocol.Astm.Records.ASTMMessage import LISMessage
from colorama import Fore, Style, init
from utility import log_to_file
import time

init()    

if __name__ == '__main__':
    message1 = [
        "H|\\^&|BS240|MINDRAY|Mindray BS-240|123 Healthcare Ave^^Mumbai^MH^400001|Lab Manager|+919876543210|CAPS-A|LabSystem|Clinical Chemistry|P|1.2.1|20250626140530|",
        "P|1|12345||67890|SHARMA^RAJESH^KUMAR|PATEL|19850315|M|I|402 Tower A^^Mumbai^MH^400052||+919988776655|DR001|INS12345|POL67890|178|72|HTN^DM|Amlodipine^Metformin|Vegetarian^Diabetic|CARDIO|REF001|20250625^20250627|Outpatient|General Ward",
        "O|1|GLU01||^^^GLU^Glucose||20250626080000|||||F||||1||||||||||O",
        "R|1|^^^GLU^Glucose|125.5|mg/dL|70_99|H||F||tech001|20250626081500||V1.0|MINDRAY BS-240",
        "L|1|N"
    ]

    message2 = [
        "H|\\^&|BS240|MINDRAY|Mindray BS-240|123 Healthcare Ave^^Mumbai^MH^400001|Lab Manager|+919876543210|CAPS-A|LabSystem|Clinical Chemistry|P|1.2.1|20250626140531|",
        "P|1|12346||67891|DESAI^MEENA^KUMARI|DESAI|19751222|F|I|903 Garden Rd^^Pune^MH^411001||+918855443322|DR002|INS12346|POL67891|162|60|Hypothyroidism||Vegetarian|ENDO|REF002|20250626^20250627|Outpatient|Endocrine Ward",
        "O|1|TSH01||^^^TSH^Thyroid Stimulating Hormone||20250626081000|||||F||||1||||||||||O",
        "L|1|N"
    ]

    message3 = [
        "H|\\^&|BS240|MINDRAY|Mindray BS-240|123 Healthcare Ave^^Mumbai^MH^400001|Lab Manager|+919876543210|CAPS-A|LabSystem|Clinical Chemistry|P|1.2.1|20250626140532|",
        "P|1|12347||67892|KHAN^AAMIR^ALI|KHAN|19900310|M|I|58 Street Lane^^Nagpur^MH^440001||+917777888999|DR003|INS12347|POL67892|180|75|High Cholesterol||Non-Vegetarian|LIPID|REF003|20250626^20250627|Outpatient|General Ward",
        "O|1|CHOL01||^^^CHOL^Cholesterol||20250626083000|||||F||||1||||||||||O",
        "L|1|N"
    ]

    message4 =  [
        "H|\\^&|BS240|MINDRAY|Mindray BS-240|123 Healthcare Ave^^Mumbai^MH^400001|Lab Manager|+919876543210|CAPS-A|LabSystem|Clinical Chemistry|P|1.2.1|20250626140530|",
        "P|1|12345||67890|SHARMA^RAJESH^KUMAR|PATEL|19850315|M|I|402 Tower A^^Mumbai^MH^400052||+919988776655|DR001|INS12345|POL67890|178|72|HTN^DM|Amlodipine^Metformin|Vegetarian^Diabetic|CARDIO|REF001|20250625^20250627|Outpatient|General Ward",
        "O|1|GLU01||^^^GLU^Glucose||20250626080000|||||F||||1||||||||||O",
        "R|1|^^^GLU^Glucose|125.5|mg/dL|70_99|H||F||tech001|20250626081500||V1.0|MINDRAY BS-240",
        "L|1|N"
    ]

    messages = [
        message1,
        message2,
        message3,
        message4
    ]

    framed_astm = frame_astm_message(messages)

    # ==========     Send over serial or print     ==========
    # for frame in framed_astm:
    #     print(f"{Fore.GREEN}{repr(frame)}{Style.RESET_ALL} : {Fore.YELLOW}{len(frame)}{Style.RESET_ALL}\n")
    #     print()
    # ==========     XXXXXXXXXXXXXXXXXXXXXXXXX     ==========


    # print("sleeping for 2 seconds")
    # time.sleep(2)

    print("Running tests")
    
    # Query message
    analyzerOpt1 = [
        "H|\\^&|||Mindry^^|||||||QR|1394-97|20250606135727\r"
        "P|23|||||||||||||||||||||||||||||||||\r"
        "O|23|||P^P||20250606114816|||||2^mlt cntrl2^059425004^20270201^8.770000^M^0.430000^5.560562||||||||||||||F|||||\r"
        "L|23|N"
    ]
    analyzerOutput = [ analyzerOpt1 ]

    # Suppose the list[list[str]] is coming from the client

    framedOutput:list[bytes] = frame_astm_message(analyzerOutput) 
    for f in framedOutput:
        print(f"frame:{f}  length: {len(f)}")

    try:
        records = enhanced_decode(framedOutput)
        # lisObj = LISMessage()
        # lis_message = lisObj.create_lis_obj(records)
        # json_string = lis_message.to_json()
        # filepath = log_to_file(json_string, "Logs", "decoded_data_log")
        # print(f"successfully added data in file: {Fore.GREEN}{repr(filepath)}{Style.RESET_ALL}\n")

    except Exception as e:
        print(f"Debug error: {e.with_traceback()}")