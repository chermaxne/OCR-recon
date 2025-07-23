Traceback (most recent call last):
  File "c:\Github\OCR-recon\pythonscript", line 46, in <module>
    print(f"Line: '{line.content}' Polygon: {poly}")
                    ^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'content' import os
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv("ENDPOINT")    
key = os.getenv("KEY")              

if not endpoint or not key:
    raise ValueError("Please set ENDPOINT and KEY in your .env file")

client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def is_inside_region(polygon, target_region):
    def to_float(val):
        return val.x if hasattr(val, "x") else val

    for i in range(0, len(polygon), 2):
        x = to_float(polygon[i])
        y = to_float(polygon[i + 1])
        if not (target_region["x_min"] <= x <= target_region["x_max"] and
                target_region["y_min"] <= y <= target_region["y_max"]):
            return False
    return True



# Hardcoded region for "First Name" field
first_name_region = {
    "x_min": 0.75,
    "x_max": 2.09,
    "y_min": 1.67,
    "y_max": 1.85
}

with open("test_statement_individual.pdf", "rb") as f:
    poller = client.begin_analyze_document("prebuilt-document", document=f)
    result = poller.result()

first_name = None

for line in result.content:
    poly = [(p.x, p.y) for p in line.polygon] if hasattr(line, "polygon") else []
    print(f"Line: '{line.content}' Polygon: {poly}")
    
# Loop through all content elements (paragraphs, lines, etc.)
for line in result.content:
    if hasattr(line, "polygon") and is_inside_region(line.polygon, first_name_region):
        first_name = line.content
        print("First Name found:", first_name)
        break

print("First Name:", first_name)
