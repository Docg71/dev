
class I2C_ADDR:
    
    ADDR_GROVE_HAT		= 0x08
    ADDR_UART_HAT 		= 0x48		# Can also show UU, then has an overlay in /boot/firmware/config.txt
    ADDR_I2C_EXT 		=-0x70		# I2C Extender
    ADDR_PARTICLE_CNT	= 0x40
    
    ADDR_INPUT_MODULE	= 0x20		# iNPUT AND OUTPUT MODULE HAVE THE SAME IC 
    ADDR_OUTPUT_MODULE  = 0x20		# iNPUT AND OUTPUT MODULE HAVE THE SAME IC
    ADDR_BARO_SENSOR	= 0x77
    ADDR_16X2_LCD		= 0x3E
    
    ADDR_OLED_NAS		= 0x3C
    
    




class TCA_Const_A:

# constants
    TCA_CHANNEL_LCD16x2 	= 0x01
    TCA_CHANNEL_GAS_SENSOR	= 0x02
    TCA_CHANNEL_BAROMETER	= 0x04
    TCA_CHANNEL_3=0x08
    TCA_CHANNEL_4=0x10
    TCA_CHANNEL_5=0x20
    TCA_CHANNEL_6=0x40
    TCA_CHANNEL_7=0x80
    TCA_CHANNEL_NONE=0x00
    TCA_CHANNEL_ALL=0xFF
    
    