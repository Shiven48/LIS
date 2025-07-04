import hl7
import json
from datetime import datetime

def parse_obx_segments(segments):
    results = []
    for seg in segments:
        # Strip whitespace from segment type
        seg_type = str(seg[0]).strip() if seg[0] else ""
        if seg_type != 'OBX':
            continue
        
        # Handle test_id and test_name safely
        test_id = seg[3][0] if len(seg[3]) > 0 else ""
        test_name = seg[3][1] if len(seg[3]) > 1 else ""
        
        obx = {
            "sequence": seg[1],
            "value_type": seg[2],
            "test_id": test_id,
            "test_name": test_name,
            "value": seg[5],
            "units": seg[6],
            "reference_range": seg[7],
            "flags": seg[8],
        }
        results.append(obx)
    return results

def parse_hl7_message(message: str):
    print("Debug: Starting to parse HL7 message")
    parsed = hl7.parse(message)
    print(f"Debug: Number of segments parsed: {len(parsed)}")
    message_dict = {
        "msh": {},
        "pid": {},
        "pv1": {},
        "obr": {},
        "obx_results": []
    }
    
    for seg in parsed:
        # Strip whitespace from segment type - this is the key fix
        seg_type = str(seg[0]).strip() if seg[0] else ""
        print(f"Debug: Segment type: '{seg_type}' (original: '{seg[0]}'), Length: {len(seg)}, First few fields: {seg[:5]}")
        
        if seg_type == 'MSH':
            message_dict["msh"] = {
                "sending_app": seg[2] if len(seg) > 2 else "",
                "sending_facility": seg[3] if len(seg) > 3 else "",
                "datetime": seg[6] if len(seg) > 6 else "",
                "message_type": seg[8] if len(seg) > 8 else "",
                "message_id": seg[9] if len(seg) > 9 else "",
                "hl7_version": seg[11] if len(seg) > 11 else "",
            }
        elif seg_type == 'PID':
            message_dict["pid"] = {
                "patient_id": seg[1] if len(seg) > 1 else "",
            }
        elif seg_type == 'PV1':
            message_dict["pv1"] = {
                "visit_number": seg[1] if len(seg) > 1 else "",
            }
        elif seg_type == 'OBR':
            # Handle OBR test_id and test_name safely
            test_id = seg[4][0] if len(seg) > 4 and len(seg[4]) > 0 else ""
            test_name = seg[4][1] if len(seg) > 4 and len(seg[4]) > 1 else ""
            
            message_dict["obr"] = {
                "order_id": seg[3] if len(seg) > 3 else "",
                "test_id": test_id,
                "test_name": test_name,
                "ordered_at": seg[6] if len(seg) > 6 else "",
                "collected_at": seg[7] if len(seg) > 7 else "",
            }
    
    message_dict["obx_results"] = parse_obx_segments(parsed)
    return message_dict

if __name__ == "__main__":

    # This is the point where the info will be fetched
    raw_message = r"MSH|^~\&|ELite 580|Erba|||20250616082505||ORU^R01|b514d88f2eab4d5980eea27a7408ea6d|P|2.3.1||||||UNICODE" + "\r\n" + r"PID|1||||||||||||||||||||||||||||||" + "\r\n" + r"PV1|1|||||||||||||||||||||||||||||||||||||||||||||" + "\r\n" + r"OBR|1||2025000716|01001^Automated Count^99MRC||20250616043136|20250616043136|||||||20250616043136||||||||20250616054751||HM||||admin||||admin" + "\r\n" + r"OBX|1|IS|02001^Take Mode^99MRC||A||||||F" + "\r\n" + r"OBX|2|IS|02002^Blood Mode^99MRC||W||||||F" + "\r\n" + r"OBX|3|IS|02003^Test Mode^99MRC||CBC+DIFF||||||F" + "\r\n" + r"OBX|4|NM|30525-0^Age^LN||||||||F" + "\r\n" + r"OBX|5|IS|09001^Remark^99MRC||||||||F" + "\r\n" + r"OBX|6|IS|03001^Ref Group^99MRC||General||||||F" + "\r\n" + r"OBX|7|NM|6690-2^WBC^LN||3.35|10*3/uL|4.00-10.00|L~A|||F" + "\r\n" + r"OBX|8|NM|770-8^NEU%^LN||58.3|%|50.0-70.0|~N|||F" + "\r\n" + r"OBX|9|NM|736-9^LYM%^LN||35.2|%|20.0-40.0|~N|||F" + "\r\n" + r"OBX|10|NM|5905-5^MON%^LN||5.0|%|3.0-12.0|~N|||F" + "\r\n" + r"OBX|11|NM|713-8^EOS%^LN||1.0|%|0.5-5.0|~N|||F" + "\r\n" + r"OBX|12|NM|706-2^BAS%^LN||0.5|%|0.0-1.0|~N|||F" + "\r\n" + r"OBX|13|NM|751-8^NEU#^LN||1.96|10*3/uL|2.00-7.00|L~A|||F" + "\r\n" + r"OBX|14|NM|731-0^LYM#^LN||1.18|10*3/uL|0.80-4.00|~N|||F" + "\r\n" + r"OBX|15|NM|742-7^MON#^LN||0.16|10*3/uL|0.12-1.20|~N|||F" + "\r\n" + r"OBX|16|NM|711-2^EOS#^LN||0.03|10*3/uL|0.02-0.50|~N|||F" + "\r\n" + r"OBX|17|NM|704-7^BAS#^LN||0.02|10*3/uL|0.00-0.10|~N|||F" + "\r\n" + r"OBX|18|NM|26477-0^*ALY#^LN||0.00|10*3/uL|0.00-0.20|~N|||F" + "\r\n" + r"OBX|19|NM|13046-8^*ALY%^LN||0.1|%|0.0-2.0|~N|||F" + "\r\n" + r"OBX|20|NM|11001^*LIC#^99MRC||0.00|10*3/uL|0.00-0.20|~N|||F" + "\r\n" + r"OBX|21|NM|11002^*LIC%^99MRC||0.1|%|0.0-2.5|~N|||F" + "\r\n" + r"OBX|22|NM|789-8^RBC^LN||5.16|10*6/uL|3.50-5.50|~N|||F" + "\r\n" + r"OBX|23|NM|718-7^HGB^LN||13.3|g/dL|11.0-16.0|~N|||F" + "\r\n" + r"OBX|24|NM|4544-3^HCT^LN||39.3|%|37.0-54.0|~N|||F" + "\r\n" + r"OBX|25|NM|787-2^MCV^LN||76.2|fL|80.0-100.0|L~A|||F" + "\r\n" + r"OBX|26|NM|785-6^MCH^LN||25.7|pg|27.0-34.0|L~A|||F" + "\r\n" + r"OBX|27|NM|786-4^MCHC^LN||33.7|g/dL|32.0-36.0|~N|||F" + "\r\n" + r"OBX|28|NM|788-0^RDW-CV^LN||13.5|%|11.0-16.0|~N|||F" + "\r\n" + r"OBX|29|NM|21000-5^RDW-SD^LN||36.9|fL|35.0-56.0|~N|||F" + "\r\n" + r"OBX|30|NM|777-3^PLT^LN||199|10*3/uL|100-300|~N|||F" + "\r\n" + r"OBX|31|NM|32623-1^MPV^LN||10.8|fL|6.5-12.0|~N|||F" + "\r\n" + r"OBX|32|NM|32207-3^PDW-SD^LN||13.3|fL|9.0-17.0|~N|||F" + "\r\n" + r"OBX|33|NM|11090^PDW-CV^LN||16.4|%|10.0-17.9|~N|||F" + "\r\n" + r"OBX|34|NM|11003^PCT^99MRC||0.216|%|0.108-0.282|~N|||F" + "\r\n" + r"OBX|35|NM|48386-7^P-LCR^LN||32.9|%|11.0-45.0|~N|||F" + "\r\n" + r"OBX|36|NM|34167-7^P-LCC^LN||65|10*9/L|30-90|~N|||F"
    
    structured_result = parse_hl7_message(raw_message)
    
    with open("parsed_result.json", "w") as out:
        json.dump(structured_result, out, indent=2)
    
    print("HL7 parsed successfully to parsed_result.json")
    
    print("\nSample parsed data:")
    print(f"Message Type: {structured_result['msh'].get('message_type', 'N/A')}")
    print(f"Sending Application: {structured_result['msh'].get('sending_app', 'N/A')}")
    print(f"Number of OBX results: {len(structured_result['obx_results'])}")
    if structured_result['obx_results']:
        print(f"First test result: {structured_result['obx_results'][0]['test_name']} = {structured_result['obx_results'][0]['value']}")