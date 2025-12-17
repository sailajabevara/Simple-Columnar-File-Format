import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from src.writer import write_custom_file


def main():
    if len(sys.argv) != 3:
        print("Usage: python csv_to_custom.py <input.csv> <output.colm>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_file = sys.argv[2]

    write_custom_file(input_csv, output_file)
    print("CSV converted to custom columnar format successfully!")


if __name__ == "__main__":
    main()
