__all__ = ["main", "usage"]

import sys
import os

COMMANDS = ('read', 'write', 'chksum', 'verify', 'identify')

def usage():
  name = os.path.basename(sys.argv[0])
  print("Usage:\n\
  {0} read <outout_filename> [address[:size]]\n\
  {0} write <input_filename> [address[:size]]\n\
  {0} chksum [address[:size]]\n\
  {0} verify <input_filename> [address[:size]]\n".format(name));

def main():
  if len(sys.argv) < 2:
    return usage()

  command = sys.argv[1].lower()

  if command not in COMMANDS:
    return usage()

  func = getattr(sys.modules[__name__], command, None)
  if func is None:
    print("{0} is currently unsupported.\n".format(command))
    return

  spi = spidev.SpiDev()
  return func(spi, **sys.argv[2:])


def identify(spi, *args):
  print("Identifying eeprom chip...")
  _eeprom_address(spi, 0x5555)
  _eeprom_data(spi, 0xAA)
  _eeprom_write_pulse(spi)

  # sleep for 40ns... (Tblc)

  _eeprom_address(spi, 0x2AAA)
  _eeprom_data(spi, 0x55)
  _eeprom_write_pulse(spi)

  # sleep for 40ns... (Tblc)

  _eeprom_address(spi, 0x5555)
  _eeprom_data(spi, 0x90)
  _eeprom_write_pulse(spi)

  #read in manuf id (should be 0xBF)
  _eeprom_address(spi, 0x0)
  spi.open(0,1)
  spi.xfer2([0x41, 0x19, 0x3]) # WE high, CE low, OE low


def _eeprom_address(spi, addr):
  spi.open(0,0)
  # write A0..A7
  spi.xfer2([0x41, 0x9, addr & 0xFF])
  # A8 .. A15
  spi.xfer2([0x41, 0x19, (addr & 0xFF00) >> 8])

def _eeprom_data(spi, data):
  spi.open(0, 1)
  # D0..D7
  spi.xfer2([0x41, 0x9, data & 0xFF])

def __eeprom_write_pulse(spi):
  spi.open(0, 1)
  # A16 . . . . WE CE OE

  byte = 0x1  # CE low, OE high, WE low
  spi.xfer2([0x41, 0x19, byte])

  # sleep for 40ns... (Twp)

  byte = 0x5  # CE low, OE high, WE high
  spi.xfer2([0x41, 0x19, byte])
