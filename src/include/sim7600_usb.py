
# for SIM7600  4g DTU with USB
# https://www.waveshare.com/wiki/SIM7600G-H_4G_DTU

# See also https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT


''' Some basicc omc
AT	AT Test Command	OK
ATE	ATE1 set echo
ATE0 close echo	OK
AT+CGMI	Query module manufacturer	OK
AT+CGMM	Query module model	OK
AT+CGSN	Query product serial number	OK
AT+CSUB	Query module version and chip	OK
AT+CGMR	Query the firmware version serial number	OK
AT+IPREX	Set the module hardware serial port baud rate	+IPREX:
OK
AT+CRESET	Reset module	OK
AT+CSQ	Network signal quality query, return signal value	+CSQ: 17,99
OK
AT+CPIN?	Query the status of the SIM card and return READY, indicating that the SIM card can be recognized normally	+CPIN: READY
AT+COPS?	Query the current operator, the operator information will be returned after normal networking	+COPS:
OK
AT+CREG?	Query network registration status	+CREG:
OK
AT+CPSI?	Query UE system information	
AT+CNMP?	Network mode selection command：
2: Automatic
13: GSM only
38: LTE only
48: Any modes but LTE
'''

'''
Question:What is the function of the com port for ttyUSB0-ttyUSB5 that appears under the Linux system?
 Answer:
As shown below:
1) /dev/ttyUSB0-diag port for output developing messages
2) /dev/ttyUSB1- NMEA port for GPS NMEA data output
3) /dev/ttyUSB2-AT port for AT commands
4) /dev/ttyUSB3-Modem port for ppp-dial
5) /dev/ttyUSB4-Audio port

'''








