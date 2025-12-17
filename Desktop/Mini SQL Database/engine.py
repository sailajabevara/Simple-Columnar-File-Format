import csv
import os


class Table:
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.name = self._extract_table_name(csv_file_path)
        self.rows = self._load_csv(csv_file_path)

    def _extract_table_name(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[0]

    def _load_csv(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        rows = []

        with open(file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise ValueError("CSV file must have a header row")

            for row in reader:
                rows.append(dict(row))

        if not rows:
            raise ValueError("CSV file is empty")

        return rows
