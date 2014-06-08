
class EepromProgrammer(object):

  def __init__(self):
    self.OE = 1
    self.CE = 1
    self.WE = 1
    self.ADDR = 0x0


    self.io = IOExpander32()
    # port A   -> a0..a7
    # port B   -> a8..a15
    # Port C   -> d0..d7
    # port D.0 -> a16
    # port D.5 -> WE#
    # port D.6 -> OE#
    # port D.7 -> CE#

    # set up address pins and control lines as outputs
    self.io.setPortDirection(IOExpander32.PORT_A, 0)
    self.io.setPortDirection(IOExpander32.PORT_B, 0)
    self.io.setPortDirection(IOExpander32.PORT_D, 0)

  def writePage(self, pageAddress, bytes):
    self.CE = 0
    self.OE = 1
    self.WE = 1
    self.io.setPortDirection(IOExpander32.PORT_C, 0x0)  # data lines as outputs
    self.syncBits()
    self._write_address(0x5555, 0xAA)
    self._write_address(0x2AAA, 0x55)
    self._write_address(0x5555, 0xA0)
    for i in min(128, range(0, len(bytes))):
      self._write_address(pageAddress+i, bytes[i])

  def readBytes(self, startingAddress, size):
    WE = 1
    CE = 0
    OE = 0
    self.ADDR = startingAddress
    self.io.setPortDirection(IOExpander32.PORT_C, 0xFF)  # data lines as inputs
    self.syncBits()

    bytes = []
    for i in range(0,size):
      bytes.append(self._read_address(startingAddress+i))
    return bytes

  def _read_address(self, address):
    self.ADDR = address
    self.syncBits()
    return readData()

  def _write_address(self, address, value):
    self.ADDR = address
    self.writeData(value)
    self.syncBits()
    self.WE_pulse()

  def WE_pulse(self):
    self.WE = 0
    self.syncBits()
    # pause for long enough...
    self.WE = 1
    self.syncBits()

  def syncBits(self):
    self.io.writePort(IOExpander32.PORT_A, self.ADDR & 0xFF)
    self.io.writePort(IOExpander32.PORT_B, (self.ADDR & 0xFF00) >> 8)

    dvalue = (self.CE & 1)<<7 | (self.OE & 1)<<6 | (self.WE & 1)<<5 | ((self.ADDR & 0x10000)>>16)
    self.io.writePort(IOExpander32.PORT_D, dvalue)

  def writeData(self, value):
    self.io.writePort(IOExpander32.PORT_C, value)    

  def readData(self):
    return self.io.readPort(IOExpander32.PORT_C)

