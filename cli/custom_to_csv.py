import sys
import os
import csv

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from src.reader import read_custom_file


def main():
    if len(sys.argv) != 3:
        print("Usage: python custom_to_csv.py <input.colm> <output.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    headers, rows = read_custom_file(input_file)

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print("Custom file converted back to CSV successfully!")


if __name__ == "__main__":
    main()
