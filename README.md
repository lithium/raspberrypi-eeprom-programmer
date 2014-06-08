raspberrypi-eeprom-programmer
=============================


A tool to Read/Write EEPROMs with raspberry pi and MCP23S18 I/O expansion ports.

The EEPROM in question to program for this project was the Greenliant GLS29EE010. A 1Mbit (128k x8) EEPROM. this chip requires 28 i/o pins to fully drive the chip. (17 address, 8 data, OE, CE and WE)

Two MCP23S18 SPI I/O expansion ports are used to shit data in and out of the EEPROM from the pi's SPI ports.



Schematic
---------
```
  GPIO10 (MOSI) -> MCP-A/MCP-B pin 14 (SI)
  GPIO09 (MISO) -> MCP-A/MCP-B pin 15 (SO)
  GPIO11 (CLK)  -> MCP-A/MCP-B pin 13 (SCK)
  GPIO8  (CE0)  -> MCP-A pin 12 (CS#)
  GPIO7  (CE1)  -> MCP-B pin 12 (CS#)

  MCP-A GPA0:GPA7 -> EEPROM A0:A7
  MCP-A GPB0:GPB7 -> EEPROM A8:A15
  MCP-B GPA0 -> EEPROM CE#
  MCP-B GPA1 -> EEPROM OE#
  MCP-B GPA2 -> EEPROM WE#
  MCP-B GPA7 -> EEPROM A16
  MCP-B GPB0:GPB7 -> EEPROM D0:D7
```



Tool Usage
----------

```rasbpi-eeprom read <outout_filename> [address[:size]]```  
```rasbpi-eeprom write <input_filename> [address[:size]]```  
```rasbpi-eeprom chksum [address[:size]]```  
```rasbpi-eeprom verify <input_filename> [address[:size]]```  


