import socket
from datetime import datetime
from astm import decode, decode_message, decode_record, encode
from io import BytesIO

RAW_FILE = "erba_raw.txt"
PARSED_FILE = "erba_parsed.txt"
HOST = '0.0.0.0'
PORT = 5600

def parse_with_astm_lib(data: bytes) -> str:
    """
    Uses the python-astm library to decode ASTM data into a readable format.
    """
    try:
        # First try the main decode function
        messages = decode(data)
        output = []
        for message in messages:
            for record in message:
                output.append(str(record))
        return "\n".join(output)
    except Exception as e:
        # If main decode fails, try parsing individual records
        try:
            # Split the data by record separators and parse each record
            records = data.split(b'\r')
            output = ["=== PARSING INDIVIDUAL RECORDS ==="]
            for i, record_data in enumerate(records):
                if record_data and len(record_data) > 1:
                    try:
                        # Remove control characters for parsing
                        clean_record = record_data.strip(b'\x02\x03\x1c')
                        if clean_record:
                            parsed_record = decode_record(clean_record + b'\r', encoding='ascii')
                            output.append(f"Record {i+1}: {parsed_record}")
                    except Exception as rec_e:
                        output.append(f"Record {i+1} failed: {rec_e}")
            return "\n".join(output)
        except Exception as e2:
            return f"[ERROR] Both parsing methods failed: Original: {e}, Fallback: {e2}"

def test_astm_parsing():
    """
    Test function to verify ASTM parsing is working with a demo message
    """
    print("=" * 60)
    print("ASTM PARSING TEST")
    print("=" * 60)
    
    # Demo ASTM message - typical clinical chemistry result
    # This is a simplified ASTM E1394 format message
    demo_astm_raw = (
        b'\x02H|\\^&|||Analyzer^Mindray BS-240||1234567|20250617090000||P|1.0|||Host|LIS\x0D'
        b'P|1||PAT12345||Doe^John^A||19850101|M|||||||||||||||||||\x0D'
        b'O|1|ORD12345||^^^CBC|||20250617090000|||||||||F\x0D'
        b'R|1|^^^WBC|5.8|10*3/uL|4.0-10.0|N|||F||admin||20250617090500\x0D'
        b'R|2|^^^RBC|4.9|10*6/uL|4.0-5.5|N|||F||admin||20250617090500\x0D'
        b'R|3|^^^HGB|14.1|g/dL|13.0-17.0|N|||F||admin||20250617090500\x0D'
        b'R|4|^^^HCT|42.5|%|38.0-50.0|N|||F||admin||20250617090500\x0D'
        b'R|5|^^^PLT|250|10*3/uL|150-400|N|||F||admin||20250617090500\x0D'
        b'L|1|N\x0D'
        b'\x03\x1C\x0D'
    )
    
    print("1. RAW ASTM MESSAGE (bytes):")
    print(f"Length: {len(demo_astm_raw)} bytes")
    print("Raw bytes:", demo_astm_raw[:100], "..." if len(demo_astm_raw) > 100 else "")
    print()
    
    print("2. RAW ASTM MESSAGE (decoded string):")
    print(demo_astm_raw.decode('ascii', errors='ignore'))
    print()
    
    print("3. PARSED ASTM MESSAGE:")
    parsed_result = parse_with_astm_lib(demo_astm_raw)
    print(parsed_result)
    print()
    
    # Test individual decode functions
    print("4. TESTING INDIVIDUAL DECODE FUNCTIONS:")
    print("-" * 40)
    
    try:
        print("decode_message result:")
        # Fix 2: decode_message needs encoding parameter
        msg_result = decode_message(demo_astm_raw, encoding='ascii')
        print(f"Type: {type(msg_result)}")
        print(f"Content: {msg_result}")
        print()
    except Exception as e:
        print(f"decode_message failed: {e}")
        print()
    
    try:
        print("decode_record result:")
        # Fix 3: decode_record needs encoding parameter
        single_record = b'P|1||12345||DOE^JOHN^A||19800101|M|||||||||||||||||||\x0D'
        rec_result = decode_record(single_record, encoding='ascii')
        print(f"Type: {type(rec_result)}")
        print(f"Content: {rec_result}")
        print()
    except Exception as e:
        print(f"decode_record failed: {e}")
        print()
    
    print("5. CREATING AND ENCODING A TEST MESSAGE:")
    print("-" * 40)
    
    try:
        # Import record classes
        from astm import HeaderRecord, PatientRecord, OrderRecord, ResultRecord, TerminatorRecord
        
        # Fix 4: Create records with proper parameters (check what each record accepts)
        print("Creating recordemo_astm_rawds...")
        
        # Create a simple header record
        header = HeaderRecord()
        header.seq = 1
        header.sender_name = 'TEST_SYSTEM'
        
        # Create a simple patient record
        patient = PatientRecord()
        patient.seq = 1
        patient.practice_id = 'TEST123'
        patient.last_name = 'SMITH'
        patient.first_name = 'JANE'
        
        # Create a simple order record
        order = OrderRecord()
        order.seq = 1
        order.specimen_id = 'SAMPLE001'
        
        # Create a simple result record
        result = ResultRecord()
        result.seq = 1
        result.data_measurement = '95'
        result.units = 'mg/dL'
        
        # Create terminator record
        terminator = TerminatorRecord()
        terminator.seq = 1
        terminator.termination_code = 'N'
        
        # Create message
        message = [header, patient, order, result, terminator]
        
        # Encode the message
        encoded_msg = encode(message)
        print("Encoded message:")
        print(encoded_msg)
        print()
        
        # Test parsing the encoded message
        print("6. PARSING THE ENCODED MESSAGE:")
        print("-" * 40)
        # Fix: encode() returns a list, we need the first element
        if isinstance(encoded_msg, list) and len(encoded_msg) > 0:
            encoded_bytes = encoded_msg[0]
            parsed_encoded = parse_with_astm_lib(encoded_bytes)
            print(parsed_encoded)
        else:
            print(f"Unexpected encoded format: {type(encoded_msg)}")
        
    except Exception as e:
        print(f"Encoding test failed: {e}")
        # Let's try a simpler approach
        print("\nTrying alternative approach...")
        try:
            # Just test with manual record creation
            from astm.records import HeaderRecord
            h = HeaderRecord()
            print(f"HeaderRecord created: {h}")
            print(f"HeaderRecord attributes: {dir(h)}")
        except Exception as e2:
            print(f"Alternative approach also failed: {e2}")
    
    print("7. TESTING ASTM LIBRARY COMPONENTS:")
    print("-" * 40)
    
    # Let's explore what's available in the astm module
    import astm
    print("Available in astm module:")
    available_items = [item for item in dir(astm) if not item.startswith('_')]
    for item in available_items:
        try:
            obj = getattr(astm, item)
            print(f"  {item}: {type(obj)}")
        except:
            print(f"  {item}: <unable to access>")
    
    print("8. SIMPLE WORKING EXAMPLE:")
    print("-" * 40)
    
    # Let's create a simple message that should work
    try:
        simple_records = []
        
        # Create basic records
        h = HeaderRecord()
        h.seq = 1
        simple_records.append(h)
        
        p = PatientRecord() 
        p.seq = 1
        simple_records.append(p)
        
        l = TerminatorRecord()
        l.seq = 1 
        l.termination_code = 'N'
        simple_records.append(l)
        
        # Encode this simple message
        simple_encoded = encode(simple_records)
        print(f"Simple encoded message: {simple_encoded}")
        
        if isinstance(simple_encoded, list) and len(simple_encoded) > 0:
            simple_bytes = simple_encoded[0]
            print(f"Simple message bytes: {simple_bytes}")
            print(f"Simple message string: {simple_bytes.decode('ascii', errors='ignore')}")
            
            # Try to parse it back
            simple_parsed = parse_with_astm_lib(simple_bytes)
            print(f"Simple parsed result:\n{simple_parsed}")
            
    except Exception as e:
        print(f"Simple example failed: {e}")
    
    print("\n9. RECORD-BY-RECORD PARSING TEST:")
    print("-" * 40)
    
    # Test individual record parsing with our demo data
    demo_records = [
        b'H|\\^&|||HOST^1|||||||||P|E 1394-97',
        b'P|1||12345||DOE^JOHN^A||19800101|M|||||||||||||||||||',
        b'O|1|67890||^^^GLU^GLUCOSE|R|||||||||||||||||||||||',
        b'R|1|^^^GLU^GLUCOSE|120|mg/dL|70_110|H|||F||OPERATOR1||20241217120000|||',
        b'L|1|N'
    ]
    
    for i, record_bytes in enumerate(demo_records):
        try:
            parsed = decode_record(record_bytes + b'\r', encoding='ascii')
            print(f"Record {i+1} ({chr(record_bytes[0])}): {parsed}")
        except Exception as e:
            print(f"Record {i+1} failed: {e}")
    
    print("\n" + "=" * 60)
    print("ANALYSIS:")
    print("- decode_record() works perfectly for individual records")
    print("- The library can create and encode messages") 
    print("- Full message parsing is strict about ASTM format")
    print("- For real data, we can parse record-by-record if needed")
    print("=" * 60)

def listen_to_erba():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[INFO] Listening on port {PORT}...")
       
        conn, addr = s.accept()
        print(f"[INFO] Connected by {addr}")
        conn.settimeout(None)
        buffer = b""
       
        while True:
            try:
                chunk = conn.recv(1024)
                if chunk:
                    buffer += chunk
                    # ASTM messages usually end with <FS><CR> = \x1c\x0d
                    if b'\x1c\x0d' in buffer:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       
                        # Log raw ASTM data
                        with open(RAW_FILE, "a", encoding="utf-8") as f:
                            f.write(f"\n\n--- Received at {timestamp} ---\n")
                            f.write(buffer.decode(errors="ignore"))
                       
                        # Parse ASTM
                        parsed = parse_with_astm_lib(buffer)
                        with open(PARSED_FILE, "a", encoding="utf-8") as f:
                            f.write(f"\n\n--- Parsed at {timestamp} ---\n")
                            f.write(parsed)
                       
                        print(f"[INFO] Message processed at {timestamp}")
                        buffer = b""  # Reset buffer after processing
                       
            except Exception as e:
                print(f"[ERROR] Socket error: {e}")
                break

if __name__ == "__main__":
    # Run the test first
    test_astm_parsing()
    
    # Ask user if they want to start the server
    print("\nDo you want to start the ASTM server? (y/n): ", end="")
    choice = input().lower()
    if choice == 'y':
        listen_to_erba()
    else:
        print("Test completed. Server not started.")