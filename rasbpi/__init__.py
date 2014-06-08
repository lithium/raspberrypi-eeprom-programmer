__all__ = ["EepromCommandLine", "EepromProgrammer", "IOExpander32"]

import sys
import os
import rasbpi
from IOExpander import *
from EepromProgrammer import *

class EepromCommandLine(object):
  COMMANDS = ('read', 'write', 'chksum', 'verify')

  def __init__(self):
    self.programmer = rasbpi.EepromProgrammer()

  def usage(self):
    name = os.path.basename(sys.argv[0])
    print("Usage:\n\
    {0} read <outout_filename> [address[:size]]\n\
    {0} write <input_filename> [address[:size]]\n\
    {0} chksum [address[:size]]\n\
    {0} verify <input_filename> [address[:size]]\n".format(name));

  def main(self):
    if len(sys.argv) < 2:
      return self.usage()

    command = sys.argv[1].lower()

    if command not in self.COMMANDS:
      return self.usage()

    func = getattr(self, command, None)
    if func is None:
      print("{0} is currently unsupported.\n".format(command))
      return


    return func(*sys.argv[2:])

  def write(self, filename, address=0, size=1):
    self.programmer.writePage(address, [0x55]);
    print "wrote 0x55 to address %x" %(address,)

  def read(self, filename, address=0, size=1):
    #print "read into %s from %x for %d bytes" % (filename, address, size)
    byte = self.programmer.readBytes(address,size)
    print "read %s from address %x" % (byte,address)

