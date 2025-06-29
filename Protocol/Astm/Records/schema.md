# ASTM Records Specification - Client and Server Side

## `Header Record`

### Client Header Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias      | Example Value        |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 3.1.1        | Record Type ID               | `type`             | `H`                  |
| 2  | 3.1.2        | Delimiter Definition         | `delimiters`       | `\^&`                |
| 3  | 3.1.3        | Message Control ID           | `message_id`       | `MSG001`             |
| 4  | 3.1.4        | Access Password              | `password`         |                      |
| 5  | 3.1.5        | Sender Name/ID               | `sender_id`        | `CLIENT_LAB`         |
| 6  | 3.1.6        | Sender Street Address        | `sender_address`   |                      |
| 7  | 3.1.7        | Reserved                     | `reserved`         |                      |
| 8  | 3.1.8        | Sender Phone Number          | `sender_phone`     |                      |
| 9  | 3.1.9        | Characteristics              | `characteristics`  |                      |
| 10 | 3.1.10       | Receiver ID                  | `receiver_id`      | `SERVER_LAB`         |
| 11 | 3.1.11       | Comments                     | `comments`         |                      |
| 12 | 3.1.12       | Processing ID                | `processing_id`    | `P`                  |
| 13 | 3.1.13       | Version Number               | `version`          | `1`                  |
| 14 | 3.1.14       | Date and Time                | `timestamp`        | `20231201120000`     |

**Client ASTM:** `H|\^&|MSG001||CLIENT_LAB|||||SERVER_LAB||P|1|20231201120000`

### Server Header Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias      | Example Value        |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 3.1.1        | Record Type ID               | `type`             | `H`                  |
| 2  | 3.1.2        | Delimiter Definition         | `delimiters`       | `\^&`                |
| 3  | 3.1.3        | Message Control ID           | `message_id`       | `MSG001`             |
| 4  | 3.1.4        | Access Password              | `password`         |                      |
| 5  | 3.1.5        | Sender Name/ID               | `sender_id`        | `SERVER_LAB`         |
| 6  | 3.1.6        | Sender Street Address        | `sender_address`   | `123 Lab St`         |
| 7  | 3.1.7        | Reserved                     | `reserved`         |                      |
| 8  | 3.1.8        | Sender Phone Number          | `sender_phone`     | `555-0123`           |
| 9  | 3.1.9        | Characteristics              | `characteristics`  |                      |
| 10 | 3.1.10       | Receiver ID                  | `receiver_id`      | `CLIENT_LAB`         |
| 11 | 3.1.11       | Comments                     | `comments`         |                      |
| 12 | 3.1.12       | Processing ID                | `processing_id`    | `P`                  |
| 13 | 3.1.13       | Version Number               | `version`          | `1`                  |
| 14 | 3.1.14       | Date and Time                | `timestamp`        | `20231201120500`     |

**Server ASTM:** `H|\^&|MSG001||SERVER_LAB|123 Lab St||555-0123||CLIENT_LAB||P|1|20231201120500`

---

## `Comment Record`

### Client Comment Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias      | Example Value        |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 4.1.1        | Record Type ID               | `type`             | `C`                  |
| 2  | 4.1.2        | Sequence Number              | `seq`              | `1`                  |
| 3  | 4.1.3        | Comment Source               | `source`           | `L`                  |
| 4  | 4.1.4        | Comment Text                 | `text`             | `Sample urgent`      |
| 5  | 4.1.5        | Comment Type                 | `comment_type`     | `G`                  |

**Client ASTM:** `C|1|L|Sample urgent|G`

### Server Comment Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias      | Example Value        |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 4.1.1        | Record Type ID               | `type`             | `C`                  |
| 2  | 4.1.2        | Sequence Number              | `seq`              | `1`                  |
| 3  | 4.1.3        | Comment Source               | `source`           | `I`                  |
| 4  | 4.1.4        | Comment Text                 | `text`             | `Results validated`  |
| 5  | 4.1.5        | Comment Type                 | `comment_type`     | `G`                  |

**Server ASTM:** `C|1|I|Results validated|G`

---

## `Order Record`

### Client Order Record Structure:

| #  | ASTM Field # | ASTM Name                       | Python Alias        | Example Value    |
|----|--------------|----------------------------------|--------------------|------------------|
| 1  | 9.1.1        | Record Type ID                  | `type`              | `O`              |
| 2  | 9.1.2        | Sequence Number                 | `seq`               | `1`              |
| 3  | 9.1.3        | Specimen ID                     | `sample_id`         | `12120001`       |
| 4  | 9.1.4        | Instrument Specimen ID          | `instrument_id`     |                  |
| 5  | 9.1.5        | Universal Test ID               | `test_codes`        | `^^NA^,^^Cl^`    |
| 6  | 9.1.6        | Priority                        | `priority`          | `R`              |
| 7  | 9.1.7        | Requested/Ordered Date & Time   | `order_datetime`    | `20011023105715` |
| 8  | 9.1.8        | Specimen Collection Date & Time | `collection_time`   | `20011023105715` |
| 9  | 9.1.9        | Collection End Time             | `collection_end`    |                  |
| 10 | 9.1.10       | Collection Volume               | `collection_volume` |                  |
| 11 | 9.1.11       | Collector ID                    | `collector_id`      |                  |
| 12 | 9.1.12       | Action Code                     | `action_code`       | `N`              |
| 13 | 9.1.13       | Danger Code                     | `danger_code`       |                  |
| 14 | 9.1.14       | Relevant Clinical Info          | `clinical_info`     |                  |
| 15 | 9.1.15       | Specimen Received Date & Time   | `received_time`     |                  |
| 16 | 9.1.16       | Specimen Descriptor             | `biomaterial`       | `S`              |
| 17 | 9.1.17       | Ordering Physician              | `physician`         |                  |
| 18 | 9.1.18       | User Field 1                    | `user_field_1`      | `CHIM`           |
| 19 | 9.1.19       | User Field 2                    | `user_field_2`      | `AXM`            |
| 20 | 9.1.20       | Laboratory Field 1              | `lab_field_1`       | `Lab1`           |
| 21 | 9.1.21       | Laboratory Field 2              | `lab_field_2`       | `12120`          |
| 22 | 9.1.22       | Report Type                     | `report_type`       | `O`              |
| 23 | 9.1.23       | Reserved                        | `reserved`          |                  |
| 24 | 9.1.24       | Laboratory Section              | `lab_name`          | `LAB2`           |

**Client ASTM:** `O|1|12120001||^^NA^,^^Cl^|R|20011023105715|20011023105715|||||N||||S||CHIM|AXM|Lab1|12120|O||LAB2`

### Server Order Record Structure:

| #  | ASTM Field # | ASTM Name                       | Python Alias        | Example Value          |
|----|--------------|----------------------------------|--------------------|------------------------|
| 1  | 9.1.1        | Record Type ID                  | `type`              | `O`                    |
| 2  | 9.1.2        | Sequence Number                 | `seq`               | `1`                    |
| 3  | 9.1.3        | Specimen ID                     | `sample_id`         | `12120001`             |
| 4  | 9.1.4        | Instrument Specimen ID          | `instrument_id`     | `INST001`              |
| 5  | 9.1.5        | Universal Test ID               | `test_codes`        | `^^NA^,^^Cl^`          |
| 6  | 9.1.6        | Priority                        | `priority`          | `R`                    |
| 7  | 9.1.7        | Requested/Ordered Date & Time   | `order_datetime`    | `20011023105715`       |
| 8  | 9.1.8        | Specimen Collection Date & Time | `collection_time`   | `20011023105715`       |
| 9  | 9.1.9        | Collection End Time             | `collection_end`    |                        |
| 10 | 9.1.10       | Collection Volume               | `collection_volume` |                        |
| 11 | 9.1.11       | Collector ID                    | `collector_id`      |                        |
| 12 | 9.1.12       | Action Code                     | `action_code`       | `N`                    |
| 13 | 9.1.13       | Danger Code                     | `danger_code`       |                        |
| 14 | 9.1.14       | Relevant Clinical Info          | `clinical_info`     |                        |
| 15 | 9.1.15       | Specimen Received Date & Time   | `received_time`     | `20011023110000`       |
| 16 | 9.1.16       | Specimen Descriptor             | `biomaterial`       | `S`                    |
| 17 | 9.1.17       | Ordering Physician              | `physician`         | `DOC001`               |
| 18 | 9.1.18       | User Field 1                    | `user_field_1`      | `CHIM`                 |
| 19 | 9.1.19       | User Field 2                    | `user_field_2`      | `AXM`                  |
| 20 | 9.1.20       | Laboratory Field 1              | `lab_field_1`       | `Lab1`                 |
| 21 | 9.1.21       | Laboratory Field 2              | `lab_field_2`       | `12120`                |
| 22 | 9.1.22       | Report Type                     | `report_type`       | `F`                    |
| 23 | 9.1.23       | Reserved                        | `reserved`          |                        |
| 24 | 9.1.24       | Laboratory Section              | `lab_name`          | `LAB2`                 |

**Server ASTM:** `O|1|12120001|INST001|^^NA^,^^Cl^|R|20011023105715|20011023105715||||N|||20011023110000|S|DOC001|CHIM|AXM|Lab1|12120|F||LAB2`

---

## `Patient Record`

### Client Patient Record Structure:

| #   | ASTM Field # | ASTM Name                        | Python Alias       | Example Value       |
|-----|--------------|----------------------------------|--------------------|---------------------|
| 1   | 8.1.1        | Record Type ID                   | `type`             | `P`                 |
| 2   | 8.1.2        | Sequence Number                  | `seq`              | `1`                 |
| 3   | 8.1.3        | Practice Assigned Patient ID     | `practice_id`      | `PAT123`            |
| 4   | 8.1.4        | Laboratory Assigned Patient ID   | `laboratory_id`    | `LAB456`            |
| 5   | 8.1.5        | Patient ID                       | `id`               | `ID789`             |
| 6   | 8.1.6        | Patient Name                     | `name`             | `DOE^JOHN`          |
| 7   | 8.1.7        | Mother's Maiden Name             | `maiden_name`      | `SMITH`             |
| 8   | 8.1.8        | Birthdate                        | `birthdate`        | `19800101`          |
| 9   | 8.1.9        | Patient Sex                      | `sex`              | `M`                 |
| 10  | 8.1.10       | Patient Race-Ethnic Origin       | `race`             | `W`                 |
| 11  | 8.1.11       | Patient Address                  | `address`          | `123 Main St^^City^ST^12345` |
| 12  | 8.1.12       | Reserved Field                   | `reserved`         |                     |
| 13  | 8.1.13       | Patient Telephone Number         | `phone`            | `123-456-7890`      |
| 14  | 8.1.14       | Attending Physician ID           | `physician_id`     | `DOC001`            |
| 15  | 8.1.15       | Special Field #1                 | `special_1`        |                     |
| 16  | 8.1.16       | Special Field #2                 | `special_2`        |                     |
| 17  | 8.1.17       | Patient Height                   | `height`           | `180`               |
| 18  | 8.1.18       | Patient Weight                   | `weight`           | `75`                |
| 19  | 8.1.19       | Patient's Known Diagnosis        | `diagnosis`        | `Hypertension`      |
| 20  | 8.1.20       | Patient's Active Medication      | `medication`       | `Lisinopril`        |
| 21  | 8.1.21       | Patient's Diet                   | `diet`             | `Low Sodium`        |
| 22  | 8.1.22       | Practice Field No. 1             | `practice_field_1` |                     |
| 23  | 8.1.23       | Practice Field No. 2             | `practice_field_2` |                     |
| 24  | 8.1.24       | Admission/Discharge Dates        | `admission_date`   | `20230601^20230610` |
| 25  | 8.1.25       | Admission Status                 | `admission_status` | `Admitted`          |
| 26  | 8.1.26       | Location                         | `location`         | `Ward 5`            |

**Client ASTM:** `P|1|PAT123|LAB456|ID789|DOE^JOHN|SMITH|19800101|M|W|123 Main St^^City^ST^12345||123-456-7890|DOC001|||180|75|Hypertension|Lisinopril|Low Sodium|||20230601^20230610|Admitted|Ward 5`

### Server Patient Record Structure:

| #   | ASTM Field # | ASTM Name                        | Python Alias       | Example Value       |
|-----|--------------|----------------------------------|--------------------|---------------------|
| 1   | 8.1.1        | Record Type ID                   | `type`             | `P`                 |
| 2   | 8.1.2        | Sequence Number                  | `seq`              | `1`                 |
| 3   | 8.1.3        | Practice Assigned Patient ID     | `practice_id`      | `PAT123`            |
| 4   | 8.1.4        | Laboratory Assigned Patient ID   | `laboratory_id`    | `LAB456`            |
| 5   | 8.1.5        | Patient ID                       | `id`               | `ID789`             |
| 6   | 8.1.6        | Patient Name                     | `name`             | `DOE^JOHN^MIDDLE`   |
| 7   | 8.1.7        | Mother's Maiden Name             | `maiden_name`      | `SMITH`             |
| 8   | 8.1.8        | Birthdate                        | `birthdate`        | `19800101`          |
| 9   | 8.1.9        | Patient Sex                      | `sex`              | `M`                 |
| 10  | 8.1.10       | Patient Race-Ethnic Origin       | `race`             | `W`                 |
| 11  | 8.1.11       | Patient Address                  | `address`          | `123 Main St^^City^ST^12345` |
| 12  | 8.1.12       | Reserved Field                   | `reserved`         |                     |
| 13  | 8.1.13       | Patient Telephone Number         | `phone`            | `123-456-7890`      |
| 14  | 8.1.14       | Attending Physician ID           | `physician_id`     | `DOC001`            |
| 15  | 8.1.15       | Special Field #1                 | `special_1`        | `INSURANCE001`      |
| 16  | 8.1.16       | Special Field #2                 | `special_2`        | `POLICY123`         |
| 17  | 8.1.17       | Patient Height                   | `height`           | `180`               |
| 18  | 8.1.18       | Patient Weight                   | `weight`           | `75`                |
| 19  | 8.1.19       | Patient's Known Diagnosis        | `diagnosis`        | `Hypertension^Diabetes` |
| 20  | 8.1.20       | Patient's Active Medication      | `medication`       | `Lisinopril^Metformin`  |
| 21  | 8.1.21       | Patient's Diet                   | `diet`             | `Low Sodium^Diabetic`   |
| 22  | 8.1.22       | Practice Field No. 1             | `practice_field_1` | `DEPT001`           |
| 23  | 8.1.23       | Practice Field No. 2             | `practice_field_2` | `REF123`            |
| 24  | 8.1.24       | Admission/Discharge Dates        | `admission_date`   | `20230601^20230610` |
| 25  | 8.1.25       | Admission Status                 | `admission_status` | `Discharged`        |
| 26  | 8.1.26       | Location                         | `location`         | `Ward 5`            |

**Server ASTM:** `P|1|PAT123|LAB456|ID789|DOE^JOHN^MIDDLE|SMITH|19800101|M|W|123 Main St^^City^ST^12345||123-456-7890|DOC001|INSURANCE001|POLICY123|180|75|Hypertension^Diabetes|Lisinopril^Metformin|Low Sodium^Diabetic|DEPT001|REF123|20230601^20230610|Discharged|Ward 5`

---

## `Result Record`

### Client Result Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias       | Example Value         |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 12.1.1       | Record Type ID               | `type`             | `R`                  |
| 2  | 12.1.2       | Sequence Number              | `seq`              | `1`                  |
| 3  | 12.1.3       | Universal Test ID            | `test_id`          | `^^NA^`              |
| 4  | 12.1.4       | Data or Measurement Value    | `value`            | `140`                |
| 5  | 12.1.5       | Units                        | `units`            | `mmol/L`             |
| 6  | 12.1.6       | Reference Ranges             | `reference_range`  | `135-145`            |
| 7  | 12.1.7       | Result Abnormal Flags        | `abnormal_flags`   | `N`                  |
| 8  | 12.1.8       | Nature of Quality Control    | `qc_nature`        |                      |
| 9  | 12.1.9       | Date of Last Instrument Change| `last_change`     |                      |
| 10 | 12.1.10      | Instrument Identification    | `instrument_id`    |                      |
| 11 | 12.1.11      | Operator Identification      | `operator_id`      |                      |
| 12 | 12.1.12      | Date/Time Test Started       | `test_started`     | `20011023105715`     |
| 13 | 12.1.13      | Date/Time Test Completed     | `test_completed`   | `20011023110000`     |
| 14 | 12.1.14      | Instrument Charge to Computer System | `instrument_charge` |                  |

**Client ASTM:** `R|1|^^NA^|140|mmol/L|135-145|N|||||20011023105715|20011023110000|`

### Server Result Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias       | Example Value         |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 12.1.1       | Record Type ID               | `type`             | `R`                  |
| 2  | 12.1.2       | Sequence Number              | `seq`              | `1`                  |
| 3  | 12.1.3       | Universal Test ID            | `test_id`          | `^^NA^`              |
| 4  | 12.1.4       | Data or Measurement Value    | `value`            | `140.5`              |
| 5  | 12.1.5       | Units                        | `units`            | `mmol/L`             |
| 6  | 12.1.6       | Reference Ranges             | `reference_range`  | `135-145`            |
| 7  | 12.1.7       | Result Abnormal Flags        | `abnormal_flags`   | `N`                  |
| 8  | 12.1.8       | Nature of Quality Control    | `qc_nature`        | `C`                  |
| 9  | 12.1.9       | Date of Last Instrument Change| `last_change`     | `20231201`           |
| 10 | 12.1.10      | Instrument Identification    | `instrument_id`    | `ANALYZER001`        |
| 11 | 12.1.11      | Operator Identification      | `operator_id`      | `TECH001`            |
| 12 | 12.1.12      | Date/Time Test Started       | `test_started`     | `20011023105715`     |
| 13 | 12.1.13      | Date/Time Test Completed     | `test_completed`   | `20011023110000`     |
| 14 | 12.1.14      | Instrument Charge to Computer System | `instrument_charge` | `CHG001`        |

**Server ASTM:** `R|1|^^NA^|140.5|mmol/L|135-145|N|C|20231201|ANALYZER001|TECH001|20011023105715|20011023110000|CHG001`

---

## `Terminator Record`

### Client Terminator Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias       | Example Value         |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 13.1.1       | Record Type ID               | `type`             | `L`                  |
| 2  | 13.1.2       | Sequence Number              | `seq`              | `1`                  |
| 3  | 13.1.3       | Termination Code             | `termination_code` | `N`                  |

**Client ASTM:** `L|1|N`

### Server Terminator Record Structure:

| #  | ASTM Field # | ASTM Name                    | Python Alias       | Example Value         |
|----|--------------|------------------------------|--------------------|----------------------|
| 1  | 13.1.1       | Record Type ID               | `type`             | `L`                  |
| 2  | 13.1.2       | Sequence Number              | `seq`              | `1`                  |
| 3  | 13.1.3       | Termination Code             | `termination_code` | `N`                  |

**Server ASTM:** `L|1|N`

---

## Notes:

### Termination Codes:
- `N` = Normal termination
- `T` = Sender aborted
- `R` = Receiver requested termination
- `E` = Unknown encoding characters
- `P` = Transmission terminated due to protocol timeout

### Key Differences Between Client and Server Records:
1. **Header Record**: Server includes more detailed sender information (address, phone)
2. **Comment Record**: Different source codes (L=Laboratory for client, I=Instrument for server)
3. **Order Record**: Server includes instrument ID, received time, and physician information
4. **Patient Record**: Server contains more complete patient information and additional fields
5. **Result Record**: Server includes quality control information, instrument details, and operator ID
6. **Terminator Record**: Identical structure for both client and server