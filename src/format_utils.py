import struct
import zlib

# ================================
# INTEGER & FLOAT PACKING
# ================================

# Pack 32-bit integer to bytes
def pack_int32(value: int) -> bytes:
    return struct.pack("<i", value)

# Unpack 32-bit integer from bytes
def unpack_int32(data: bytes, offset: int):
    value = struct.unpack_from("<i", data, offset)[0]
    return value, offset + 4


# Pack 64-bit integer to bytes (for row count, offsets)
def pack_int64(value: int) -> bytes:
    return struct.pack("<q", value)

# Unpack 64-bit integer from bytes
def unpack_int64(data: bytes, offset: int):
    value = struct.unpack_from("<q", data, offset)[0]
    return value, offset + 8


# Pack 64-bit float to bytes
def pack_float64(value: float) -> bytes:
    return struct.pack("<d", value)

# Unpack 64-bit float from bytes
def unpack_float64(data: bytes, offset: int):
    value = struct.unpack_from("<d", data, offset)[0]
    return value, offset + 8


# ================================
# STRING ENCODING / DECODING
# ================================

# Encode UTF-8 string with length prefix
def encode_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    length = len(encoded)
    return pack_int32(length) + encoded

# Decode UTF-8 string with length prefix
def decode_string(data: bytes, offset: int):
    length, offset = unpack_int32(data, offset)
    string_bytes = data[offset: offset + length]
    value = string_bytes.decode("utf-8")
    return value, offset + length


# ================================
# COMPRESSION UTILITIES (ZLIB)
# ================================

def compress_block(data: bytes) -> bytes:
    return zlib.compress(data)

def decompress_block(data: bytes) -> bytes:
    return zlib.decompress(data)
