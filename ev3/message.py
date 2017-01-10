"""Handles the messaging with EV3 and contains several functions for dealing
with message variable types.

"""


import struct

from ev3 import system_command
from ev3 import direct_command


class MessageError(Exception):
    """Subclass for reporting errors."""
    pass

def send_message_for_reply(port, msg, message_counter=0x1234):
    """Sends the message and waits for a reply. The msg is expected to be a
    sequence of bytes and it should not contain the length/message_counter
    header. Returns an sequence of bytes without the length/message_counter
    header.

    """
    if (not msg_expects_reply(msg)):
        raise MessageError('The message is not a type that expects a reply.')

    # Message length includes the two message_counter bytes.
    msg_len = 2 + len(msg)

    buf = struct.pack('<H', msg_len) + struct.pack('<H', message_counter)

    _write_bytes(port, buf)
    _write_bytes(port, msg)

    expected_len = _read_bytes(port, 2)
    reply = _read_bytes(port, struct.unpack('<H', expected_len)[0])

    if (struct.unpack('<H', reply[0:2])[0] != message_counter):
        raise MessageError('Reply message counter does not match.')

    return reply[2:]

def send_message_no_reply(port, msg, message_counter=0x1234):
    """Sends the message without waiting for a reply."""
    if (msg_expects_reply(msg)):
        raise MessageError('The message is a type that expects a reply.')

    # Message length includes the two message_counter bytes.
    msg_len = 2 + len(msg)

    buf = struct.pack('<H', msg_len) + struct.pack('<H', message_counter)

    _write_bytes(port, buf)
    _write_bytes(port, msg)

def msg_expects_reply(msg):
    """Returns True if the given message is a type that expects a reply. The
    given message should not include the length/message_counter header.

    """
    if (system_command.CommandType.SYSTEM_COMMAND_REPLY == msg[0]):
        return True

    if (direct_command.CommandType.DIRECT_COMMAND_REPLY == msg[0]):
        return True

    return False

def parse_u16(byte_seq, index):
    """Parses a u16 value at the given index from the byte_seq."""
    return struct.unpack('<H', byte_seq[index:index + 2])[0]

def parse_u32(byte_seq, index):
    """Parses a u32 value at the given index from the byte_seq."""
    return struct.unpack('<I', byte_seq[index:index + 4])[0]

def parse_str(byte_seq, index, length=None):
    """Parses a string of length chars."""
    if (length is None):
        return byte_seq[index:].decode('utf-8')
    else:
        return byte_seq[index:index + length].decode('utf-8')

def parse_null_terminated_str(byte_seq, index, length):
    """Parses a null-terminated string of up to length chars."""
    result = bytearray()
    for i in range(index, index + length):
        if (0x00 == byte_seq[i]):
            break
        result.extend(byte_seq[i])
    return result

def parse_float(byte_seq, index):
    """Parses a 32bit floating point number."""
    return struct.unpack('<f', byte_seq[index:index + 4])[0]

def append_float(byte_list, value):
    """Appends a 32bit floating point number."""
    byte_list.extend(struct.pack('<f', value))

def append_u8(byte_list, value):
    """Appends the given value to the list."""
    byte_list.extend(struct.pack('<B', value))

def append_u16(byte_list, value):
    """Appends the given value to the list in little-endian order."""
    byte_list.extend(struct.pack('<H', value))

def append_u32(byte_list, value):
    """Appends the given value to the list in little-endian order."""
    byte_list.extend(struct.pack('<I', value))

def append_str(byte_list, str_value):
    """Appends a null-terminated string."""
    byte_list.extend(str_value.encode('utf-8'))
    if ('\0' != str_value[-1]):
        byte_list.extend(b'\0');

def _read_bytes(port, num_bytes):
    return port.read(num_bytes)

def _write_bytes(port, byte_seq):
    port.write(byte_seq)
