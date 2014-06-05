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

  return func(sys.argv[1:])


def identify(args):
  print("Identifying eeprom chip...")