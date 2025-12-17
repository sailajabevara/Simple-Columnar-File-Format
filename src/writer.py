import csv
import struct

from src.format_utils import (
    pack_int32,
    pack_int64,
    pack_float64,
    encode_string,
    compress_block,
)

# -------------------------------------------------
# Constants – must match SPEC.md
# -------------------------------------------------

MAGIC_NUMBER = b"COLM"
VERSION = 1  # 1 byte

TYPE_INT32 = 0
TYPE_FLOAT64 = 1
TYPE_STRING = 2


# -------------------------------------------------
# Type inference for CSV columns
# -------------------------------------------------

def infer_type(values):
    """
    Infer data type for a column from string values.
    Order:
      - INT32 if all non-empty values are ints
      - FLOAT64 if all non-empty values are floats
      - STRING otherwise
    """
    non_empty = [v for v in values if v != ""]
    if not non_empty:
        return TYPE_STRING  # default

    # Try INT32
    try:
        for v in non_empty:
            int(v)
        return TYPE_INT32
    except ValueError:
        pass

    # Try FLOAT64
    try:
        for v in non_empty:
            float(v)
        return TYPE_FLOAT64
    except ValueError:
        return TYPE_STRING


# -------------------------------------------------
# Encode one column to raw bytes (before compression)
# -------------------------------------------------

def encode_column(values, type_code):
    """
    Encode a list of string values into a raw byte block
    according to the type_code, using the rules in SPEC.md.
    Returns: raw_bytes (uncompressed)
    """
    parts = []

    if type_code == TYPE_INT32:
        for v in values:
            iv = int(v) if v != "" else 0
            parts.append(pack_int32(iv))

    elif type_code == TYPE_FLOAT64:
        for v in values:
            fv = float(v) if v != "" else 0.0
            parts.append(pack_float64(fv))

    elif type_code == TYPE_STRING:
        for v in values:
            s = v if v is not None else ""
            parts.append(encode_string(s))

    else:
        raise ValueError(f"Unknown type code: {type_code}")

    return b"".join(parts)


# -------------------------------------------------
# Main writer: CSV -> Custom Columnar File
# -------------------------------------------------

def write_custom_file(csv_path: str, output_path: str) -> None:
    """
    Read a CSV file and write it to a custom columnar binary file
    using the format defined in SPEC.md.
    """

    # ---------- 1. Read CSV ----------
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)  # first row is header
        rows = list(reader)

    row_count = len(rows)
    column_count = len(headers)

    if row_count == 0:
        raise ValueError("CSV file has no data rows")

    # Transpose rows -> columns
    # rows: list of [c1, c2, c3, ...]
    # columns: list of (v1, v2, v3, ...)
    columns = list(zip(*rows))

    # ---------- 2. Infer types for each column ----------
    type_codes = [infer_type(col) for col in columns]

    # ---------- 3. Encode and compress each column ----------
    column_blocks = []  # will store metadata + compressed data

    for name, type_code, values in zip(headers, type_codes, columns):
        raw_block = encode_column(values, type_code)
        uncompressed_size = len(raw_block)
        compressed_block = compress_block(raw_block)
        compressed_size = len(compressed_block)

        column_blocks.append(
            {
                "name": name,
                "type_code": type_code,
                "compressed": compressed_block,
                "compressed_size": compressed_size,
                "uncompressed_size": uncompressed_size,
                # offset will be filled later
                "offset": None,
            }
        )

    # ---------- 4. Compute offsets for each column block ----------

    # Header size: 4 (magic) + 1 (version) + 4 (col count) + 8 (row count)
    header_size = 4 + 1 + 4 + 8

    # Metadata size: sum over all columns
    metadata_size = 0
    for col in column_blocks:
        name_bytes = col["name"].encode("utf-8")
        # 4 (name length) + len(name) + 1 (type code)
        # + 8 (offset) + 8 (compressed size) + 8 (uncompressed size)
        metadata_size += 4 + len(name_bytes) + 1 + 8 + 8 + 8

    # First data block starts right after header + metadata
    current_offset = header_size + metadata_size

    for col in column_blocks:
        col["offset"] = current_offset
        current_offset += col["compressed_size"]

    # ---------- 5. Write out the file ----------

    with open(output_path, "wb") as f:
        # ----- Header -----
        f.write(MAGIC_NUMBER)                      # 4 bytes
        f.write(struct.pack("B", VERSION))         # 1 byte
        f.write(pack_int32(column_count))          # 4 bytes
        f.write(pack_int64(row_count))             # 8 bytes

        # ----- Column Metadata -----
        for col in column_blocks:
            name_bytes = col["name"].encode("utf-8")
            name_len = len(name_bytes)

            # Column Name Length
            f.write(pack_int32(name_len))
            # Column Name
            f.write(name_bytes)
            # Data Type Code (1 byte)
            f.write(struct.pack("B", col["type_code"]))
            # Data Block Offset (int64)
            f.write(pack_int64(col["offset"]))
            # Compressed Size (int64)
            f.write(pack_int64(col["compressed_size"]))
            # Uncompressed Size (int64)
            f.write(pack_int64(col["uncompressed_size"]))

        # ----- Column Data Blocks -----
        for col in column_blocks:
            f.write(col["compressed"])
