import os
import json
from extractor import extract_lab_data_from_image

folder_path = "lbmaske/"
results = []

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(folder_path, filename)
        print(f"Processing: {filename}")

        try:
            lab_tests = extract_lab_data_from_image(image_path)
            result = {
                "file_name": filename,
                "is_success": True,
                "lab_test_data": lab_tests
            }
        except Exception as e:
            result = {
                "file_name": filename,
                "is_success": False,
                "error": str(e),
                "lab_test_data": []
            }

        results.append(result)

with open("lab_test_results.json", "w") as outfile:
    json.dump(results, outfile, indent=2)

print("\nAll lab results saved to 'lab_test_results.json'")
