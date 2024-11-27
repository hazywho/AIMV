"""
This Raspberry Pi Pico MicroPython code was developed by newbiely.com
This Raspberry Pi Pico code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pico/raspberry-pi-pico-mp3-player
"""

from machine import UART, Pin
import time

# Define constants
CMD_PLAY_NEXT = 0x01
CMD_PLAY_PREV = 0x02
CMD_PLAY_W_INDEX = 0x03
CMD_SET_VOLUME = 0x06
CMD_SEL_DEV = 0x09
CMD_PLAY_W_VOL = 0x22
CMD_PLAY = 0x0D
CMD_PAUSE = 0x0E
CMD_SINGLE_CYCLE = 0x19

DEV_TF = 0x02
SINGLE_CYCLE_ON = 0x00
SINGLE_CYCLE_OFF = 0x01

PICO_RX = 9  # The Raspberry Pi Pico pin GP9 connected to the TX of the Serial MP3 Player module
PICO_TX = 8  # The Raspberry Pi Pico pin GP8 connected to the RX of the Serial MP3 Player module

# Initialize UART with the correct pins and baud rate
mp3 = UART(1, baudrate=9600, tx=Pin(PICO_TX), rx=Pin(PICO_RX))

def mp3_command(command, dat):
    frame = bytearray(8)
    frame[0] = 0x7e                # starting byte
    frame[1] = 0xff                # version
    frame[2] = 0x06                # the number of bytes of the command without starting byte and ending byte
    frame[3] = command             #
    frame[4] = 0x00                # 0x00 = no feedback, 0x01 = feedback
    frame[5] = (dat >> 8) & 0xFF   # data high byte
    frame[6] = dat & 0xFF          # data low byte
    frame[7] = 0xef                # ending byte
    mp3.write(frame)

# Wait for the chip initialization to complete
time.sleep(0.5)

# Select the TF card
mp3_command(CMD_SEL_DEV, DEV_TF)
time.sleep(0.2)  # wait for 200ms

# Play MP3
mp3_command(CMD_PLAY, 0x0000)
# mp3_command(CMD_PAUSE, 0x0000)      # Pause mp3
# mp3_command(CMD_PLAY_NEXT, 0x0000)  # Play next mp3
# mp3_command(CMD_PLAY_PREV, 0x0000)  # Play previous mp3
# mp3_command(CMD_SET_VOLUME, 30)     # Change volume to 30

# Main loop to keep the script running
while True:
    time.sleep(0.1)  # Prevent tight loop
send = serial.Serial ("/dev/ttyAMA0", 9600)

i = [0,10,45,90,135,180,225,255,225,180,135,90,45,10,0]

while True:
 for x in i:
     send.write(bytes(x))
     print(x)
     time.sleep(1.5)