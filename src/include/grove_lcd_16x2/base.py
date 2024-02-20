#!/usr/bin/env python

'''
Display Base Class
'''
'''
__all__ = [
    "Display",
    "TYPE_CHAR",
    "TYPE_GRAY",
    "TYPE_COLOR",
    "MAX_GRAY"
]



TYPE_CHAR  = 0
TYPE_GRAY  = 1
TYPE_COLOR = 2

MAX_GRAY = 100

'''


class LCD_Base:
    '''
    All display devices should inherit this virtual class,
    which provide infrastructure such as cursor and backlight inteface, etc.
    '''
    

    
    # CONSTANTS
    
    # color define
    COLOR_WHITE       =    0
    COLOR_RED         =    1
    COLOR_GREEN       =    2
    COLOR_BLUE        =    3

    REG_MODE1      = 0x00
    REG_MODE2      = 0x01
    REG_OUTPUT     = 0x08

    # commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET =	0x04
    LCD_DISPLAYCONTROL =	0x08
    LCD_CURSORSHIFT =	0x10
    LCD_FUNCTIONSET =	0x20
    LCD_SETCGRAMADDR =	0x40
    LCD_SETDDRAMADDR =	0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT =	0x00
    LCD_ENTRYLEFT =	0x02
    LCD_ENTRYSHIFTINCREMENT =	0x01
    LCD_ENTRYSHIFTDECREMENT =	0x00

    # flags for display on/off control
    LCD_DISPLAYON =	0x04
    LCD_DISPLAYOFF =	0x00
    LCD_CURSORON =	0x02
    LCD_CURSOROFF =	0x00
    LCD_BLINKON =	0x01
    LCD_BLINKOFF =	0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE =	0x08
    LCD_CURSORMOVE =	0x00
    LCD_MOVERIGHT =	0x04
    LCD_MOVELEFT =	0x00

    # flags for function set
    LCD_8BITMODE =	0x10
    LCD_4BITMODE =	0x00
    LCD_2LINE =	0x08
    LCD_1LINE =	0x00
    LCD_5x10DOTS =	0x04
    LCD_5x8DOTS =	0x00

    
    
    # VARIABLES
    _cursor = False
    _backlight = False


    # METHODS

    def __init__(self):
        self._cursor = False
        self._backlight = False

    # To be derived
    def _cursor_on(self, en):
        pass

    def cursor(self, enable = None):
        '''
        Enable or disable the backlight on display device,
        not all device support it.

        Args:
            enable (bool): Optional, ``True`` to enable, ``Flase`` to disable.
                           if not provided, only to get cursor status.

        Returns:
            bool: cursor status, ``True`` - on, ``False`` - off.
        '''
        if type(enable) == bool:
            self._cursor = enable
            self._cursor_on(enable)
        return self._cursor

    # To be derived
    def _backlight_on(self, en):
        pass

    def backlight(self, enable = None):
        '''
        Enable or disable the cursor on display device,
        not all device support it.

        Args:
            enable (bool): Optional, ``True`` to enable, ``Flase`` to disable.
                           if not provided, only to get cursor status.

        Returns:
            bool: backlight status, ``True`` - on, ``False`` - off.
        '''
        if type(enable) == bool:
            self._backlight = enable
            self._backlight_on(enable)
        return self._backlight

