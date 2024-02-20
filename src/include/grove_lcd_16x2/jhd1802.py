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


BASE_ADDRESS = 0x3E


from .lcd_base import LCD_Base
import smbus2 as smbus
import sys
import logging



#logging.basicConfig(filename="i2c_extender", level=logging.DEBUG)
_logger = logging.getLogger("jhd1802_log")

__all__ = ["JHD1802"]



class JHD1802(LCD_Base):
    '''
    Grove - 16 x 2 LCD, using chip JHD1802.
        - Grove - 16 x 2 LCD (Black on Yellow)
        - Grove - 16 x 2 LCD (Black on Red)
        - Grove - 16 x 2 LCD (White on Blue)
  '''
        
# constants

# variables
    _address = 0x00
    _I2Cbus = None
    _name = "LCD 16x2"

# methods

    def __str__(self):
        return "Controls lcd displays with the JHD1802 chip"

    def __init__(self, address=BASE_ADDRESS, I2Cbus=None):
        super().__init__()
        self._address = address
        if I2Cbus == None:
            self._I2Cbus = smbus.SMBus(1)
            _logger.debug("SMBus Internal Init")
        else:
            _logger.debug("SMBus Progr. Init")
            
        self._channels = 0
        _logger.debug('lcd display : 0x{:02x}'.format(address))
        
        
    def IsConnected( self , OnExit = False ):
            try:
                self._I2Cbus.write_quick(self._address)
            except:
                print("Check if the {} is inserted, then try again".format(self._name))
                
                if OnExit:
                    sys.exit(1)
        
        
        
        
        
    @property
    def name(self):
        '''
        Get device name

        Returns:
            string: JHD1802
        '''
        return "JHD1802"

    def type(self):
        '''
        Get device type

        Returns:
            int: ``TYPE_CHAR``
        '''
        return TYPE_CHAR

    def size(self):
        '''
        Get display size

        Returns:
            (Rows, Columns): the display size, in characters.
        '''
        # Charactor 16x2
        # return (Rows, Columns)
        return 2, 16

    def clear(self):
        '''
        Clears the screen and positions the cursor in the upper-left corner.
        '''
        self.jhd.clear()

    def draw(self, data, bytes):
        '''
        Not implement for char type display device.
        '''
        return False

    def home(self):
        '''
        Positions the cursor in the upper-left of the LCD.
        That is, use that location in outputting subsequent text to the display.
        '''
        self.jhd.home()

    def setCursor(self, row, column):
        '''
        Position the LCD cursor; that is, set the location
        at which subsequent text written to the LCD will be displayed.

        Args:
            row   (int): the row at which to position cursor, with 0 being the first row
            column(int): the column at which to position cursor, with 0 being the first column

	Returns:
	    None
        '''
        self.jhd.setCursor(row, column)

    def write(self, msg):
        '''
        Write character(s) to the LCD.

        Args:
            msg (string): the character(s) to write to the display

        Returns:
            None
        '''
        self.jhd.write(msg)

    def _cursor_on(self, enable):
        if enable:
            self.jhd.cursorOn()
        else:
            self.jhd.cursorOff()

def main():
    import time

    lcd = JHD1802()
    rows, cols = lcd.size()
    print("LCD model: {}".format(lcd.name))
    print("LCD type : {} x {}".format(cols, rows))

    lcd.backlight(False)
    time.sleep(1)

    lcd.backlight(True)
    lcd.setCursor(0, 0)
    lcd.write("hello world!")
    lcd.setCursor(0, cols - 1)
    lcd.write('X')
    lcd.setCursor(rows - 1, 0)
    for i in range(cols):
        lcd.write(chr(ord('A') + i))

    time.sleep(3)
    lcd.clear()

if __name__ == '__main__':
    main()

