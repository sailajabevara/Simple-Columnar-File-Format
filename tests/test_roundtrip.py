import os
import filecmp
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_CSV = os.path.join(PROJECT_ROOT, "sample_data", "sample.csv")
CUSTOM_FILE = os.path.join(PROJECT_ROOT, "sample_data", "test_roundtrip.colm")
OUTPUT_CSV = os.path.join(PROJECT_ROOT, "sample_data", "roundtrip_output.csv")

CSV_TO_CUSTOM = os.path.join(PROJECT_ROOT, "cli", "csv_to_custom.py")
CUSTOM_TO_CSV = os.path.join(PROJECT_ROOT, "cli", "custom_to_csv.py")

print("Running round-trip test...")

# 1. CSV → Custom
subprocess.check_call([sys.executable, CSV_TO_CUSTOM, INPUT_CSV, CUSTOM_FILE])

# 2. Custom → CSV
subprocess.check_call([sys.executable, CUSTOM_TO_CSV, CUSTOM_FILE, OUTPUT_CSV])

# 3. Compare input & output CSV
if filecmp.cmp(INPUT_CSV, OUTPUT_CSV, shallow=False):
    print(" TEST PASSED: Round-trip CSV is identical.")
else:
    print("TEST FAILED: Output CSV is different.")
