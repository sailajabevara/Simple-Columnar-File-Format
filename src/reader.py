import struct

from src.format_utils import (
    unpack_int32,
    unpack_int64,
    unpack_float64,
    decode_string,
    decompress_block,
)

MAGIC_NUMBER = b"COLM"

TYPE_INT32 = 0
TYPE_FLOAT64 = 1
TYPE_STRING = 2


def read_custom_file(file_path: str):
    """
    Read the entire custom columnar file and reconstruct
    the full table (all columns, all rows).
    Returns: headers (list), rows (list of lists)
    """

    with open(file_path, "rb") as f:
        data = f.read()

    offset = 0

    # ---------- 1. Read Header ----------
    magic = data[offset:offset + 4]
    offset += 4

    if magic != MAGIC_NUMBER:
        raise ValueError("Invalid file format")

    version = struct.unpack_from("B", data, offset)[0]
    offset += 1

    column_count, offset = unpack_int32(data, offset)
    row_count, offset = unpack_int64(data, offset)

    # ---------- 2. Read Column Metadata ----------
    columns_meta = []

    for _ in range(column_count):
        name_len, offset = unpack_int32(data, offset)
        name_bytes = data[offset:offset + name_len]
        offset += name_len
        name = name_bytes.decode("utf-8")

        type_code = struct.unpack_from("B", data, offset)[0]
        offset += 1

        data_offset, offset = unpack_int64(data, offset)
        compressed_size, offset = unpack_int64(data, offset)
        uncompressed_size, offset = unpack_int64(data, offset)

        columns_meta.append({
            "name": name,
            "type": type_code,
            "offset": data_offset,
            "compressed_size": compressed_size,
            "uncompressed_size": uncompressed_size,
        })

    # ---------- 3. Read & Decode Each Column ----------
    decoded_columns = []

    for col in columns_meta:
        start = col["offset"]
        end = start + col["compressed_size"]
        compressed_block = data[start:end]

        raw_block = decompress_block(compressed_block)

        col_values = []
        block_offset = 0

        if col["type"] == TYPE_INT32:
            for _ in range(row_count):
                v, block_offset = unpack_int32(raw_block, block_offset)
                col_values.append(v)

        elif col["type"] == TYPE_FLOAT64:
            for _ in range(row_count):
                v, block_offset = unpack_float64(raw_block, block_offset)
                col_values.append(v)

        elif col["type"] == TYPE_STRING:
            for _ in range(row_count):
                v, block_offset = decode_string(raw_block, block_offset)
                col_values.append(v)

        else:
            raise ValueError("Unknown column type")

        decoded_columns.append(col_values)

    # ---------- 4. Reconstruct Rows ----------
    headers = [col["name"] for col in columns_meta]

    rows = []
    for i in range(row_count):
        row = [decoded_columns[c][i] for c in range(column_count)]
        rows.append(row)

    return headers, rows
def read_selected_columns(file_path: str, selected_columns: list):
    """
    Read only selected columns from the custom columnar file.
    selected_columns: list of column names to read
    Returns: headers (selected), rows (selected only)
    """

    with open(file_path, "rb") as f:
        data = f.read()

    offset = 0

    # ---------- 1. Read Header ----------
    magic = data[offset:offset + 4]
    offset += 4

    if magic != MAGIC_NUMBER:
        raise ValueError("Invalid file format")

    version = struct.unpack_from("B", data, offset)[0]
    offset += 1

    column_count, offset = unpack_int32(data, offset)
    row_count, offset = unpack_int64(data, offset)

    # ---------- 2. Read Column Metadata ----------
    columns_meta = []

    for _ in range(column_count):
        name_len, offset = unpack_int32(data, offset)
        name_bytes = data[offset:offset + name_len]
        offset += name_len
        name = name_bytes.decode("utf-8")

        type_code = struct.unpack_from("B", data, offset)[0]
        offset += 1

        data_offset, offset = unpack_int64(data, offset)
        compressed_size, offset = unpack_int64(data, offset)
        uncompressed_size, offset = unpack_int64(data, offset)

        columns_meta.append({
            "name": name,
            "type": type_code,
            "offset": data_offset,
            "compressed_size": compressed_size,
            "uncompressed_size": uncompressed_size,
        })

    # ---------- 3. Read Only Selected Columns ----------
    selected_meta = [c for c in columns_meta if c["name"] in selected_columns]

    if not selected_meta:
        raise ValueError("None of the selected columns were found")

    decoded_columns = []

    for col in selected_meta:
        start = col["offset"]
        end = start + col["compressed_size"]
        compressed_block = data[start:end]

        raw_block = decompress_block(compressed_block)

        col_values = []
        block_offset = 0

        if col["type"] == TYPE_INT32:
            for _ in range(row_count):
                v, block_offset = unpack_int32(raw_block, block_offset)
                col_values.append(v)

        elif col["type"] == TYPE_FLOAT64:
            for _ in range(row_count):
                v, block_offset = unpack_float64(raw_block, block_offset)
                col_values.append(v)

        elif col["type"] == TYPE_STRING:
            for _ in range(row_count):
                v, block_offset = decode_string(raw_block, block_offset)
                col_values.append(v)

        else:
            raise ValueError("Unknown column type")

        decoded_columns.append(col_values)

    # ---------- 4. Reconstruct Selected Rows ----------
    selected_headers = [col["name"] for col in selected_meta]

    rows = []
    for i in range(row_count):
        row = [decoded_columns[c][i] for c in range(len(selected_meta))]
        rows.append(row)

    return selected_headers, rows

