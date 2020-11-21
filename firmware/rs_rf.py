#!/usr/bin/python
import serial
import struct

from datetime import datetime

def check_datacode(datacode):
  try:
    return struct.calcsize(datacode)
  except struct.error:
    return False


def decode(datacode, frame):
  # Ensure little-endian & standard sizes used
  e = '<'

  # set the base data type to bytes
  b = 'B'

  # get data size from data code
  s = int(check_datacode(datacode))

  result = struct.unpack(e + datacode[0], struct.pack(e + b*s, *frame))
  return result[0]

def recover(sd):
  decoded = []
  bytepos = 0
  count=len(sd)//2
  for i in range(count):
      # Determine the number of bytes to use for each value by it's datacode
      size = 2
      try:
          value = decode('H', [int(v) for v in sd[bytepos:bytepos+size]])
      except Exception:
          print(f"{i} Unable to decode as values incorrect for datacode(s)")
      bytepos += size
      decoded.append(value/100)
  return decoded


ser = serial.Serial('/dev/ttyAMA0', 38400)

ser.write(b'f10')
# ser.write(b'f20')
# ser.write(b'c1')
try:
  while True:
    response = ser.readline()
  #  z = response.split(" ")
    print("{}:{}".format(datetime.now(), response))
    try:
      sd = response.decode().strip()
      if sd.startswith('OK'):
        print(recover(sd.split()[2:]))
    except UnicodeDecodeError as e:
      print(e, 'decode error, skip')
      continue
    # print("{}\n".format(datetime.now()))
    print()

except KeyboardInterrupt:
  ser.close()

