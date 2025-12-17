# Simple Columnar File Format

This project implements a **custom columnar binary file format from scratch**, inspired by analytical storage formats like **Parquet** and **ORC**.  
It demonstrates core data engineering concepts:

- Binary file layout design  
- Column-oriented storage  
- zlib compression  
- Metadata + byte offsets  
- Selective column reads  
- CSV ↔ Custom format round-trip conversion  

This project is built as part of the **Partnr Mandatory Task: Build a Simple Columnar File Format From Scratch**.

---

##  Project Structure

```
Simple-Columnar-File-Format/
│
├── spec/
│   └── SPEC.md                  # Binary file format specification
│
├── src/
│   ├── format_utils.py          # Binary + zlib helper utilities
│   ├── writer.py                # CSV → Custom columnar writer
│   └── reader.py                # Full + selective column reader
│
├── cli/
│   ├── csv_to_custom.py         # Convert CSV → Custom format
│   └── custom_to_csv.py         # Convert Custom format → CSV
│
├── tests/
│   └── test_roundtrip.py        # Automated round-trip test
│
├── sample_data/
│   ├── sample.csv               # Input CSV file
│   └── output.csv               # Output CSV after round-trip
│
├── .gitignore
└── README.md
```

---

##  Supported Data Types

The format supports the required 3 data types:

- **INT32** — 32-bit integer  
- **FLOAT64** — 64-bit floating-point  
- **STRING (UTF-8)** — variable-length strings  

---

## File Format Summary

### **1️. Header**  
Contains:

- Magic number (`COLM`)
- Version
- Number of columns
- Number of rows

---

### **2️. Column Metadata**  
Each column stores:

- Column name length + name  
- Type code  
- Offset to compressed block  
- Compressed size  
- Uncompressed size  

---

### **3️. Column Data Blocks**  
Each column’s data is:

- Stored contiguously  
- Compressed using **zlib**  
- Read independently (enables column pruning)

---

##  Usage Examples

### **Convert CSV → Custom Format**
```bash
python cli/csv_to_custom.py sample_data/sample.csv sample_data/sample.colm
```

---

### **Convert Custom Format → CSV**
```bash
python cli/custom_to_csv.py sample_data/sample.colm sample_data/output.csv
```

---

### **Selectively Read Columns**

```python
from src.reader import read_selected_columns
h, r = read_selected_columns("sample_data/sample.colm", ["name", "salary"])
print(h)
print(r)
```

**Expected output:**
```css
['name', 'salary']
[['Alice', 50000.5], ['Bob', 60000.0], ['Charlie', 45000.75], ['David', 70000.25]]
```

---

##  Round-Trip Testing

Run the automated test:

```bash
python tests/test_roundtrip.py
```

**Expected output:**
```
CSV converted to custom columnar format successfully!
Custom file converted back to CSV successfully!
TEST PASSED: Round-trip CSV is identical.
```

---

##  Resources Used

- Mockaroo – sample CSV generator  
- Columnar Databases (What, Why, How) – conceptual reference  
- Python `struct` module – binary packing/unpacking  
- zlib compression – column block compression  

---

##  Project Status

This project includes:

✔ Full binary specification  
✔ Working writer & reader  
✔ Selective column reads  
✔ CLI conversion tools  
✔ Round-trip test  
✔ Clean project structure  
✔ Fully documented README  

**This project is complete and ready for Partnr submission.**
