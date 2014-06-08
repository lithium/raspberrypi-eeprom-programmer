import spidev


class IOExpander32(object):
  """
    Utilize 2 MCP23S18 via spi to provide 4x 8-bit bi-directional ports

    Nomenclature: 
    PortA = spi(0,0).GPA
    PortB = spi(0,0).GPB
    PortC = spi(0,1).GPA
    PortD = spi(0,1).GPB
  """

  SPI_DEV0=(0,0)
  SPI_DEV1=(0,1)

  # these port address offsets assume chip is configured for BANK=0
  PORT_A=(SPI_DEV0,0)
  PORT_B=(SPI_DEV0,1)
  PORT_C=(SPI_DEV1,0)
  PORT_D=(SPI_DEV1,1)

  READ_OPCODE=0x41
  WRITE_OPCODE=0x40

  def __init__(self, spi=None):
    self.spi = spi if spi is not None else spidev.SpiDev()

    # config both devices the same:
    # bank=0, mirror=0, seqop=0 

  def _write_register(self, device, address, bytes):
    self.spi.open(*device)
    self.spi.xfer2([IOExpander32.WRITE_OPCODE, address] + [bytes])

  def _read_register(self, device, address):
    self.spi.open(*device)
    self.spi.xfer2([IOExpander32.READ_OPCODE, address])
    return self.spi.readbytes(1)


  def setPortDirection(self, port, value):
    self._write_register(port[0], 0x00 + port[1], value)
  def portDirection(self, port):
    return self._read_register(port[0], 0x00 + port[1])

  def setPortPolarity(self, port, value):
    self._write_register(port[0], 0x02 + port[1], value)
  def portPolarity(self, port):
    return self._read_register(port[0], 0x02 + port[1])

  def setPortPullup(self, port, value):
    self._write_register(port[0], 0x0C + port[1], value)
  def portPullup(self, port):
    return self._read_register(port[0], 0x0C + port[1])

  def readPort(self, port):
    return self._read_register(port[0], 0x12 + port[1])
  def writePort(self, port, value):
    self._write_register(port[0], 0x12 + port[1], value)

  def readLatches(self, port):
    return self._read_register(port[0], 0x14 + port[1])
  def writeLatches(self, port, value):
    self._write_register(port[0], 0x14 + port[1], value)
