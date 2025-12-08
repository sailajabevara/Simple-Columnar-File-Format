# Simple Columnar File Format Specification

## 1. Overview
This document defines the binary specification for a custom columnar file format.  
The format stores tabular data in a column-oriented layout with zlib compression and supports efficient selective column reads.

---

## 2. File Layout
The file is divided into three main sections in the following order:

1. File Header  
2. Column Metadata Section  
3. Column Data Blocks  

Overall structure:

[Header]  
[Column Metadata for all columns]  
[Compressed Column Data Blocks]

---

## 3. Endianness
All numeric values in this file are stored in **little-endian** byte order.

---

## 4. Supported Data Types

| Type Code | Data Type | Description |
|-----------|-----------|-------------|
| 0 | INT32 | 32-bit signed integer |
| 1 | FLOAT64 | 64-bit floating-point number |
| 2 | STRING | Variable-length UTF-8 encoded string |

---

## 5. File Header Structure

| Field Name | Size (Bytes) | Description |
|------------|--------------|-------------|
| Magic Number | 4 | Fixed file identifier "COLM" |
| Version | 1 | File format version |
| Column Count | 4 | Total number of columns (INT32) |
| Row Count | 8 | Total number of rows (INT64) |

---

## 6. Column Metadata Structure (Repeated for Each Column)

| Field Name | Size (Bytes) | Description |
|------------|--------------|-------------|
| Column Name Length | 4 | Length of column name in bytes |
| Column Name | Variable | UTF-8 encoded column name |
| Data Type Code | 1 | Column data type code |
| Data Block Offset | 8 | Byte offset from start of file to column data block |
| Compressed Size | 8 | Size of compressed column block in bytes |
| Uncompressed Size | 8 | Size of raw uncompressed column data |

This metadata section stores the schema (column names and data types) and the exact byte offsets required to directly seek to any column’s data block.

---

## 7. Column Data Blocks

Each column’s values are stored as a **separate contiguous block** and then compressed using **zlib**.

### 7.1 INT32 Columns
Values are stored as consecutive 4-byte integers in little-endian format.  
Total raw size = Number of rows × 4 bytes.

### 7.2 FLOAT64 Columns
Values are stored as consecutive 8-byte floating-point numbers in little-endian format.  
Total raw size = Number of rows × 8 bytes.

### 7.3 STRING Columns
Each string value is stored as:
[4-byte string length] + [UTF-8 encoded string bytes]

All string values for a column are concatenated sequentially before compression.

---

## 8. Compression
Each column’s raw data block is compressed independently using the **zlib compression algorithm**.  
Both the compressed and uncompressed sizes are recorded in the column metadata.

---

## 9. Selective Column Reading
The reader parses the column metadata to obtain each column’s byte offset and block size.  
To read only selected columns, the reader directly seeks to the required offsets and decompresses only those blocks without scanning the full file.

---

## 10. Example Logical View

Example CSV:

id,name,age  
1,Alice,20  
2,Bob,22  

The file will contain:
- One header
- Three column metadata entries (id, name, age)
- Three compressed column data blocks stored separately
