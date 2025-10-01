import time
import xml.etree.ElementTree as ET
from pathlib import Path


# --- Data Parsing ---
def parse_xml_to_json(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    sms_list = []
    for i, sms_element in enumerate(root.findall("sms")):
        sms_list.append(
            {
                "id": i,
                "protocol": sms_element.get("protocol"),
                "address": sms_element.get("address"),
                "date": sms_element.get("date"),
                "type": sms_element.get("type"),
                "subject": sms_element.get("subject"),
                "body": sms_element.get("body"),
                "toa": sms_element.get("toa"),
                "sc_toa": sms_element.get("sc_toa"),
                "service_center": sms_element.get("service_center"),
                "read": sms_element.get("read"),
                "status": sms_element.get("status"),
                "locked": sms_element.get("locked"),
                "date_sent": sms_element.get("date_sent"),
                "sub_id": sms_element.get("sub_id"),
                "readable_date": sms_element.get("readable_date"),
                "contact_name": sms_element.get("contact_name"),
            }
        )
    return sms_list


# Get the path to the XML file relative to this script
xml_file_path = (
    Path(__file__).parent.parent / "database" / "raw" / "modified_sms_v2.xml"
)
transactions = parse_xml_to_json(xml_file_path)
transactions_dict = {t["id"]: t for t in transactions}


# --- DSA Integration ---
def linear_search(transaction_id):
    start_time = time.time()
    for t in transactions:
        if t["id"] == transaction_id:
            return time.time() - start_time, t
    return time.time() - start_time, None


def dictionary_lookup(transaction_id):
    start_time = time.time()
    transaction = transactions_dict.get(transaction_id)
    return time.time() - start_time, transaction


def measure_time():
    linear_times = []
    dict_times = []
    for i in range(min(20, len(transactions))):
        linear_time, _ = linear_search(i)
        dict_time, _ = dictionary_lookup(i)
        linear_times.append(linear_time)
        dict_times.append(dict_time)
    avg_linear_time = sum(linear_times) / len(linear_times)
    avg_dict_time = sum(dict_times) / len(dict_times)
    print(f"Average Linear Search Time: {avg_linear_time:.10f} seconds")
    print(f"Average Dictionary Lookup Time: {avg_dict_time:.10f} seconds")


if __name__ == "__main__":
    measure_time()
