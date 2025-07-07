import re

def preprocess_text(raw_text: str) -> str:
    cleaned_text = re.sub(r"Có giá trị đến\s*\d{2}/\d{2}/\d{4}\s*Date of\s*expiry", "", raw_text, flags=re.IGNORECASE)


    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text


def extract_info(text: str) -> dict:
    info = {
        "id_number": None,
        "full_name": None,
        "dob": None,
        "origin": None,
        "residence": None,
        "expiry_date": None
    }

    # ID Number
    id_match = re.search(r"\b\d{12}\b", text)
    if id_match:
        info["id_number"] = id_match.group()

    # Full Name
    name_patterns = [
        r"Họ và tên[/\s]*Full name[:\s]*([A-ZÀ-ỸĐ\s]+)",
        r"Full name[:\s]*([A-ZÀ-ỸĐ\s]+)",
        r"Họ và tên[:\s]*([A-ZÀ-ỸĐ\s]+)",
        r"([A-ZÀ-ỸĐ]{2,}\s+[A-ZÀ-ỸĐ\s]+)"
    ]
    for pattern in name_patterns:
        name_match = re.search(pattern, text, re.IGNORECASE)
        if name_match:
            full_name = name_match.group(1).strip()

            full_name = re.split(r"Ngày sinh|Date of birth|Giới tính|Sex|Nam|Nữ|Male|Female", full_name, flags=re.IGNORECASE)[0].strip()
            if len(full_name) > 3 and not re.search(r'\d', full_name):
                info["full_name"] = full_name
                break

    # Date of Birth
    dob_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
    if dob_match:
        info["dob"] = dob_match.group()

    # Place of Origin
    origin_patterns = [
        r"Quê quán[/\s]*Place of origin[:\s]*([^\n]+)",
        r"Place of origin[:\s]*([^\n]+)",
        r"Quê quán[:\s]*([^\n]+)"
    ]

    for pattern in origin_patterns:
        origin_match = re.search(pattern, text, re.IGNORECASE)
        if origin_match:
            origin = origin_match.group(1).strip()
            if len(origin) > 3:
                info["origin"] = re.sub(r'\s+', ' ', origin)
                break

    # Place of Residence
    residence_match = re.search(r"Nơi thường trú[/\s]*Place of residence[:\s]*(.*)", text, re.IGNORECASE)
    if residence_match:
        residence = residence_match.group(1).strip()

        residence = re.sub(r'\s+', ' ', residence)
        if len(residence) > 5:
            info["residence"] = residence


    # Expiry Date
    expiry_patterns = [
        r"Có\s*giá trị đến\s*(\d{2}/\d{2}/\d{4})",
        r"Date\s*of\s*expiry\s*(\d{2}/\d{2}/\d{4})"
    ]

    for pattern in expiry_patterns:
        expiry_match = re.search(pattern, text, re.IGNORECASE)
        if expiry_match:
            info["expiry_date"] = expiry_match.group(1)
            break

    return info


def clean_extracted_info(info: dict) -> dict:
    cleaned_info = info.copy()

    # Full name
    if cleaned_info.get("full_name"):
        name = re.sub(r'[^A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ\s]', '', cleaned_info["full_name"], flags=re.IGNORECASE)
        cleaned_info["full_name"] = re.sub(r'\s+', ' ', name).strip()

    # Origin
    if cleaned_info.get("origin"):
        cleaned_info["origin"] = re.sub(r'\s+', ' ', cleaned_info["origin"]).strip()

    # Residence
    if cleaned_info.get("residence"):
        residence = re.sub(r'(Có giá trị đến|Date of expiry).*', '', cleaned_info["residence"], flags=re.IGNORECASE)
        cleaned_info["residence"] = re.sub(r'\s+', ' ', residence).strip()

    # ID Number
    if cleaned_info.get("id_number"):
        id_number = re.sub(r'\D', '', cleaned_info["id_number"])
        cleaned_info["id_number"] = id_number if len(id_number) == 12 else None

    # dob
    for date_field in ["dob", "expiry_date"]:
        if cleaned_info.get(date_field):
            date = re.sub(r'[^\d/]', '', cleaned_info[date_field])
            if re.match(r'\d{2}/\d{2}/\d{4}', date):
                cleaned_info[date_field] = date
            else:
                cleaned_info[date_field] = None

    return cleaned_info


def process_identity_text(raw_text: str) -> dict:
    flattened_text = raw_text.replace('\n', ' ')

    residence_text = ""
    extracted_expiry_date = None
    residence_pattern = r"Nơi thường trú\s*I\s*Place of residence[:\s]*(.*?)(Có giá trị đến\s*(\d{2}/\d{2}/\d{4})\s*Date of\s*expiry\s*)(.*?)(?=Quê quán|Place of origin|Họ và tên|Full name|Ngày sinh|Date of birth|$)"

    match = re.search(residence_pattern, flattened_text, re.IGNORECASE)
    if match:
        addr1 = match.group(1).strip()
        extracted_expiry_date = match.group(3) # Lấy expiry_date từ Group 3
        addr2 = match.group(4).strip()
        residence_text = f"{addr1} {addr2}".strip()
        flattened_text = flattened_text.replace(match.group(0), "")

    cleaned_text = re.sub(r'\s+', ' ', flattened_text).strip()

    extracted_info = extract_info(cleaned_text)

    if residence_text and len(residence_text) > 5:
        extracted_info["residence"] = residence_text

    if extracted_expiry_date:
        extracted_info["expiry_date"] = extracted_expiry_date

    final_info = clean_extracted_info(extracted_info)

    return final_info