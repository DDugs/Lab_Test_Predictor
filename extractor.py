import pytesseract
import cv2
import re
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_lab_data_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    lab_tests = []
    pattern = re.compile(
        r"(?P<test_name>[A-Za-z \(\)\-/]+?)\s+(?P<value>[-+]?\d*\.?\d+)\s*(?P<units>[a-zA-Z/%]*)\s*(?P<ref_range>[\d\.\-–]+)?"
    )

    for line in lines:
        match = pattern.search(line)
        if match:
            data = match.groupdict()
            ref_range = data.get("ref_range", "")
            out_of_range = False

            try:
                low, high = map(float, re.split(r"[-–]", ref_range))
                val = float(data["value"])
                out_of_range = val < low or val > high
            except:
                low = high = None

            lab_tests.append({
                "test_name": data["test_name"].strip(),
                "value": data["value"],
                "units": data.get("units", "").strip(),
                "bio_reference_range": ref_range,
                "lab_test_out_of_range": out_of_range
            })

    return lab_tests
