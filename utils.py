import os
import easyocr
from openpyxl import load_workbook
import datetime

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_path):
    result = reader.readtext(image_path)
    return [text[1] for text in result]

def generate_test_cases(test_type, count, ui_elements, template_path):
    wb = load_workbook(template_path)
    ws = wb.active

    for i in range(int(count)):
        row = [f"{test_type} - TC_{i+1}", "Verify", "", "", "", "", "", "", "", ""]
        if i < len(ui_elements):
            row[2] = f"Validate {ui_elements[i]}"
        ws.append(row)

    output_path = os.path.join("output", f"TestCases_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
    wb.save(output_path)
    return output_path
