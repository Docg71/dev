#!/usr/bin/env python

'''
This is the code for
    - `Grove - 16 x 2 LCD (Black on Red) <https://www.seeedstudio.com/Grove-16-x-2-LCD-Black-on-Re-p-3197.html>`_
    - `Grove - 16 x 2 LCD (Black on Yellow) <https://www.seeedstudio.com/Grove-16-x-2-LCD-Black-on-Yello-p-3198.html>`_
    - `Grove - 16 x 2 LCD (White on Blue) <https://www.seeedstudio.com/Grove-16-x-2-LCD-White-on-Blu-p-3196.html>`_

Examples:

    .. code-block:: python

        import time
        from grove.factory import Factory

        # LCD 16x2 Characters
        lcd = Factory.getDisplay("JHD1802")
        rows, cols = lcd.size()
        print("LCD model: {}".format(lcd.name))
        print("LCD type : {} x {}".format(cols, rows))

        lcd.setCursor(0, 0)
        lcd.write("hello world!")
        lcd.setCursor(0, cols - 1)
        lcd.write('X')
        lcd.setCursor(rows - 1, 0)
        for i in range(cols):
            lcd.write(chr(ord('A') + i))

        time.sleep(3)
        lcd.clear()
'''

# Device I2C Address
BASE_ADDRESS 	=	0x3e
LCD_ADDRESS     =	0x3e
RGB_ADDRESS     =	0x62
RGB_ADDRESS_V5  =	0x30


DEST_CMD_REG	= 	0x80
DEST_DATA_REG	=	0x40                                                   


from lcd_base import LCD_Base
import smbus2 as smbus
import time
import sys
import logging



#logging.basicConfig(filename="i2c_extender", level=logging.DEBUG)
_logger = logging.getLogger("jhd1313_log")

__all__ = ["JHD1313"]



class JHD1313(LCD_Base):
    '''
    Grove - 16 x 2 LCD, using chip JHD1313 with onboard RGB controller.
        - Grove - 16 x 2 LCD (Black on Yellow)
        - Grove - 16 x 2 LCD (Black on Red)
        - Grove - 16 x 2 LCD (White on Blue)
  '''
        
# constants

# variables
    _address = 0x00
    _rgb_address = 0x00
    _I2Cbus = None
    _name = "LCD 16x2"
    
    
# private

    _displayfunction = 0
    _displaycontrol = 0
    _displaymode = 0 

    _initialized = 0

    _numlines = 0
    _currline = 0
    
    _cols = 0
    _rows = 0 

    
# methods

    def __str__(self):
        return "Controls lcd displays with the JHD1313/1802 chip"

    def __init__(self, address=LCD_ADDRESS, rgb_address=RGB_ADDRESS, I2Cbus=None):
        super().__init__()
        
        self._address = address
        
        if rgb_address != None:
            self._rgb_address = rgb_address
        
        
        if I2Cbus == None:
            self._I2Cbus = smbus.SMBus(1)
            _logger.debug("SMBus Internal Init. Calls SMBUS.open()")
        else:
            _logger.debug("SMBus Progr. Init")
            
        self._channels = 0
        
        _logger.debug('lcd display : 0x{:02x}'.format(address))
        _logger.debug('rgb controller : 0x{:02x}'.format(rgb_address))
            
        
    def IsConnected( self , address=LCD_ADDRESS, OnExit = False ):
        try:
            self._I2Cbus.write_quick(address)
            return True
        except:
            print("Check if the {} is inserted, then try again".format(self._name))
            
            if OnExit:
                sys.exit(1)
            else:
                return False
        
        
                

    def begin(self, cols,rows, lines , dotsize ):
        
        self.cols = cols
        self.rows = rows
        
        
        if lines > 1:
            self._displayfunction |= self.LCD_2LINE
        
        self._numlines = lines
        self._currline = 0

        # for some 1 line displays you can select a 10 pixel high font
        if ( dotsize != 0 ) and ( lines == 1 ):
            self._displayfunction |= self.LCD_5x10DOTS
    
        '''
            SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
            according to datasheet, we need at least 40ms after power rises above 2.7V
            before sending commands. Arduino can turn on way befer 4.5V so we'll wait 50
        '''
        time.sleep(50/1000)
        
        '''
            this is according to the hitachi HD44780 datasheet
            page 45 figure 23
        '''
  #      self._I2Cbus.write_block_data( )
  #      self._I2Cbus.write_i2c_block_data()            
            
            
        # Send function set command sequence
        self._I2Cbus.write_i2c_block_data( self._address, 0, [DEST_CMD_REG, self.LCD_FUNCTIONSET | self._displayfunction ])
        time.sleep( 5/1000) 	#  # wait more than 4.1ms

        # second try
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_FUNCTIONSET | self._displayfunction ])
        time.sleep( 2/1000) 	#  # wait more than150 us

        # third go
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_FUNCTIONSET | self._displayfunction ])
        time.sleep( 1/1000) 	#  # no need to wait


        # finally, set # lines, font size, etc.
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_FUNCTIONSET | self._displayfunction ])

        # turn the display on with no cursor or blinking default
        self.display()

        # clear it off
        self.clear()

        # Initialize to default text direction (for romance languages)
        self._displaymode = self. LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        # set the entry mode
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_ENTRYMODESET | self._displaymode ] )

        if self.IsConnected(address = RGB_ADDRESS_V5 , OnExit = False):
            #self._rgb_chip_addr = RGB_ADDRESS_V5
            self.setReg(0x00, 0x07) # reset the chip
            time.sleep(2/1000)

            self.setReg(0x04, 0x15)
            
            # set all led always on

            self.setColorWhite()

            '''
            rgb_chip_addr = RGB_ADDRESS
            # backlight init
            setReg(REG_MODE1, 0)
            # set LEDs controllable by both PWM and GRPPWM registers
            setReg(REG_OUTPUT, 0xFF)
            # set MODE2 values
            # 0010 0000 -> 0x20  (DMBLNK to 1, ie blinky mode)
            setReg(REG_MODE2, 0x20)
            '''
     


    def clear(self):
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_CLEARDISPLAY])

        self.command()
        time.sleep(2)     # this command takes a long time!
        
    def home(self):
        self.command(LCD_RETURNHOME)        # set cursor position to zero
        time.sleep(2)     # this command takes a long time!

    def SetCursor(self, col , row = 0):
        if row == 0 :
            col = col | 0x80
        else:    
            col = col | 0xc0
        
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, col])


    def noDisplay(self):
        self._displaycontrol &= ~self.LCD_DISPLAYON
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_DISPLAYCONTROL | self._displaycontrol])


    def display(self):
        self._displaycontrol |= self.LCD_DISPLAYON
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_DISPLAYCONTROL | self._displaycontrol])


    def noBlink(self):
        self._displaycontrol &= ~self.LCD_BLINKON
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_DISPLAYCONTROL | self._displaycontrol])


    def blink(self):
        self._displaycontrol |= self.LCD_BLINKON
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_DISPLAYCONTROL | self._displaycontrol])
  
         
    def noCursor(self):
        _displaycontrol &= ~self.LCD_CURSORON
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_DISPLAYCONTROL | self._displaycontrol])
    
    
    def cursor(self):
        _displaycontrol |= self.LCD_CURSORON
        self._I2Cbus.write_block_data( self._address, None, [DEST_CMD_REG, self.LCD_DISPLAYCONTROL | self._displaycontrol])
        
    def scrollDisplayLeft(self):
        self._I2Cbus.write_block_data( [ self._address,  self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT ] )
        
    def scrollDisplayRight(self):
        self._I2Cbus.write_block_data( [ self._address, self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT ] )
        
    def leftToRight(self):
        self._displaymode |= LCD_ENTRYLEFT
        self._I2Cbus.write_block_data( [ self._address, self.LCD_ENTRYMODESET | self._displaymode ])
    
    def rightToLeft(self):
        self._displaymode &= ~LCD_ENTRYLEFT
        self._I2Cbus.write_block_data( [ self._address, LCD_ENTRYMODESET | self._displaymode ] )
    
    def autoscroll(self):
        self._displaymode |= LCD_ENTRYSHIFTINCREMENT
        self._I2Cbus.write_block_data( [ self._address, LCD_ENTRYMODESET | self._displaymode ])

    def noAutoscroll(self):
        self._displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self._I2Cbus.write_block_data( [ self._address, LCD_ENTRYMODESET | self._displaymode ])
    
    '''
    def createChar(uint8_t, uint8_t[]):
         location &= 0x7 # we only have 8 locations 0-7
    command(LCD_SETCGRAMADDR | (location << 3))


    unsigned char dta[9]
    dta[0] = 0x40
    for (int i = 0 i < 8 i++) {
        dta[i + 1] = charmap[i]
    }
    i2c_send_byteS(dta, 9)

    '''
    '''
    def setCursor(uint8_t, uint8_t):
    
    
    
    # color control
    def setRGB( self , R, G , B): # set rgb
    def setPWM( self , color, pwm): # set pwm

    def setColor( self,  color ):
    def setColorAll(self):
        setRGB(0, 0, 0):
    
    def setColorWhite(self):
        setRGB(255, 255, 255):
    

    # blink the LED backlight
    def blinkLED(self):
          if (rgb_chip_addr == RGB_ADDRESS_V5)
    {
        # attach all led to pwm1
        # blink period in seconds = (<reg 1> + 2) *0.128s
        # pwm1 on/off ratio = <reg 2> / 256
        setReg(0x04, 0x2a)  # 0010 1010
        setReg(0x01, 0x06)  # blink every second
        setReg(0x02, 0x7f)  # half on, half off
    }
    def noBlinkLED(self):
       if (rgb_chip_addr == RGB_ADDRESS_V5)
    {
        setReg(0x04, 0x15)  # 0001 0101
    }
                
# Private methods otherwise resolved

    def setReg(unsigned char addr, unsigned char dta):


    def setRGB(self, r, g, b) 
        #if (rgb_chip_addr == RGB_ADDRESS_V5)
    
        self.setReg(0x06, r)
        self.setReg(0x07, g)
        self.setReg(0x08, b)
    '''
    '''
    }
    else
    {
        setReg(0x04, r)
        setReg(0x03, g)
        setReg(0x02, b)
    }
    '''











def main():
  pass


if __name__ == '__main__':
    main()

