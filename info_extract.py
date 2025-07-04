import re

def extract_info(text: str) -> dict:
    info = {
        "id_number": None,
        "full_name": None,
        "dob": None,
        "origin": None,
        "residence": None,
        "expiry_date": None
    }

    id_match = re.search(r"\b\d{9,12}\b", text)
    if id_match:
        info["id_number"] = id_match.group()

    name_match = re.search(r"Họ và tên.*?:\s*(.*)", text, re.IGNORECASE)
    if name_match:
        info["full_name"] = name_match.group(1).strip()

    dob_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    if dob_match:
        info["dob"] = dob_match.group(1)

    origin_match = re.search(r"Quê quán.*?:\s*(.*)", text, re.IGNORECASE)
    if origin_match:
        info["origin"] = origin_match.group(1).strip()

    residence_match = re.search(r"Nơi thường trú.*?:\s*(.*)", text, re.IGNORECASE)
    if residence_match:
        info["residence"] = residence_match.group(1).strip()

    expiry_match = re.search(r"Có giá trị đến.*?(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)
    if expiry_match:
        info["expiry_date"] = expiry_match.group(1)

    return info
