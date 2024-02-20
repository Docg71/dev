#!/usr/bin/env python

'''
The grove board i2c extender with the TCA 9548 chip
build on SMbus2 with i2c support.
smBus2 comes also with asyncio support. idea to build in ?

Build on the libs of seeed studio Grove.py
import os

'''


import logging
import site
import settings_i2c


#print( p.Path.cwd())
site.addsitedir('./include/')
site.addsitedir('./include/grove_lcd_16x2')


from grove_lcd_16x2 import *

#import include.grove_i2c_extender as i2cext
from grove_i2c_extender import *

'''
#from __future__ import print_function
#import time
import smbus2 as smbus
#import smbus2_asyncio

'''

#logging.basicConfig(filename="i2c_extender", level=logging.DEBUG)
_logger = logging.getLogger("totempole_log")



def main():
    
  
    
    
    # Call first on base address
    i2cExtender_1 = TCA9548A()
    
    i2cExtender_1.IsConnected(OnExit = True)
    i2cExtender_1.Enable_channel( TCA9548A.TCA_CHANNEL_0 | TCA9548A.TCA_CHANNEL_1 | TCA9548A.TCA_CHANNEL_2 )
    
    i2cExtender_1.Status_channels()
    i2cExtender_1.Disable_all()
    i2cExtender_1.Enable_all()
    
    
    
    
    LCD_1 = JHD1313()
    LCD_1.IsConnected(OnExit=True)
    LCD_1.begin(16,2,2,0)
    
 
if __name__ == '__main__':
    main()
