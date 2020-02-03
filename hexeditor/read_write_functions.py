import sys
import curses
import os


def read_bytes(file_path):
    bytes_arr = None
    with open(file_path, 'rb') as f:
        bytes_arr = bytes(f.read())
    print(bytes_arr)
    return bytes_arr

def write_bytes(file_path, bytes_arr):
    with open(file_path, 'wb') as f:
        f.write(bytes_arr)

def read_data(file_path):
    if not os.path.isfile(file_path):
        raise AssertionError()
    print("OK")
    bytes_arr = read_bytes(file_path)
    data = [ b for b in bytes_arr ]
    return data

def write_data(file_path, data):
    write_bytes(file_path, "".join([ chr(b) for b in data ]))

def join_bytes(data, byte_count, little_endian=True):
	while len(data) < byte_count:
		data.append(0)
	if little_endian:
		return sum([ data[i] << 8 * i for i in range(0, byte_count) ])
	else:
		result = 0
		for i in range(0, byte_count):
			result = (result << 8) | data[i]
		return result

def split_bytes(data, byte_count, little_endian=True):
	if little_endian:
		return [ (data >> i * 8) & 0xff for i in range(0, byte_count) ]
	else:
		return [ (data >> i * 8) & 0xff for i in range(byte_count - 1, -1, -1) ]


def rep_data(data, byte_count):
	return ('%0' + str(byte_count * 2) + 'X') % data
