'''
The grove board i2c extender with the TCA 9548 chip
build on SMbus2 with i2c support.
smBus2 comes also with asyncio support. idea to build in ?

Build on the libs of seeed studio Grove.py


A2	A1 A0
LLL	112 (decimal), 70 (hexadecimal)
LLH	113 (decimal), 71 (hexadecimal)
LHL	114 (decimal), 72 (hexadecimal)
LHH	115 (decimal), 73 (hexadecimal)
HLL	116 (decimal), 74 (hexadecimal)
HLH	117 (decimal), 75 (hexadecimal)
HHL	118 (decimal), 76 (hexadecimal)
HHH	119 (decimal), 77 (hexadecimal)


#          Channel STATUS
#  -------------------------------------------------------
# ┆  B7  ┆  B6  ┆  B5  ┆  B4  ┆  B3  ┆  B2  ┆  B1  ┆  B0  ┆                                                                
# ┆-------------------------------------------------------┆
# ┆  ch7 ┆  ch6 ┆ ch5  ┆  ch4 ┆  ch3 ┆  ch2 ┆  ch1 ┆  ch0 ┆ 
# ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ  


'''

BASE_ADDRESS = 0x70

#from __future__ import print_function
#import time
import smbus2 as smbus
#import smbus2_asyncio
import logging
import sys


#logging.basicConfig(filename="i2c_extender", level=logging.DEBUG)
_logger = logging.getLogger("i2c_ext_log")

__all__ = [ 'TCA9548A' ]

class TCA9548A:

# constants
    TCA_CHANNEL_0=0x01
    TCA_CHANNEL_1=0x02
    TCA_CHANNEL_2=0x04
    TCA_CHANNEL_3=0x08
    TCA_CHANNEL_4=0x10
    TCA_CHANNEL_5=0x20
    TCA_CHANNEL_6=0x40
    TCA_CHANNEL_7=0x80
    TCA_CHANNEL_NONE=0x00
    TCA_CHANNEL_ALL=0xFF

# variables
    _address = 0x00
    _I2Cbus = None
    _name = "i2c extender 1"

# methods

    def __str__(self):
        return "Settings channels on the TCA9548A chip ( i2c extender )"

    def __init__(self, address=BASE_ADDRESS, I2Cbus=None):
        super().__init__()
        self._address = address
        if I2Cbus == None:
            self._I2Cbus = smbus.SMBus(1)
            _logger.debug("SMBus Internal Init")
        else:
            _logger.debug("SMBus Progr. Init")
            
        self._channels = 0
        _logger.debug('i2c extender address : 0x{:02x}'.format(address))
        
    def IsConnected( self , OnExit = False ):
            try:
                self._I2Cbus.write_quick(self._address)
            except:
                print("Check if the {} is inserted, then try again".format(self._name))
                
                if OnExit:
                    sys.exit(1)    

    def _get(self):
        self._channels = self._I2Cbus.read_byte(self._address)
        _logger.debug( "Value _get:{:02x}".format(self._channels) )
    
    def _set(self , value ):
        self._I2Cbus.write_byte(self._address, value)
        _logger.debug( "Value _set: 0x{:02x}".format(value) )
    
    
    def Enable_channel(self , channel):
        self._channels |= channel
        self._set(self._channels)
       
    def Disable_channel(self, channel):    
        self._channels &= ~channel
        self._set(self._channels)
        
    def Status_channels(self):
        self._get()
        _logger.debug( "Status 0x{:02x}".format(self._channels) )
        return self._channels
    
    
    def Enable_all(self):
        self._channels = self.TCA_CHANNEL_ALL
        self._set(self._channels)

    def Disable_all(self):
        self._channels = self.TCA_CHANNEL_NONE
        self._set(self._channels)




def main():
    
    # Call first on base address
    i2cExtender_1 = TCA9548A()
    
    i2cExtender_1.Enable_channel( TCA9548A.TCA_CHANNEL_0 | TCA9548A.TCA_CHANNEL_1 | TCA9548A.TCA_CHANNEL_2 )
    
    i2cExtender_1.Status_channels()
    i2cExtender_1.Disable_all()
    i2cExtender_1.Enable_all()
    
 
if __name__ == '__main__':
    main()
