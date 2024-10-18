from huskylensPythonLibrary import HuskyLensLibrary
import time
import uos
import machine
import st7789py as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random

# oled display height

 
#SPI(1) default pins
spi1_sck=10
spi1_mosi=11
spi1_miso=8     #not use
st7789_res = 12
st7789_dc  = 13
st7789_cs  = 9
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)
 
print(uos.uname())
spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
print(spi1)

class protocol:
    print("running HUSKEYLENS protocol")
    def __init__(self,mode="I2C"):   
        self.husky = HuskyLensLibrary(mode) ## SERIAL OR I2C 
        self.display = st7789.ST7789(spi1, disp_width, disp_width,
                                reset=machine.Pin(st7789_res, machine.Pin.OUT),
                                dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                                xstart=0, ystart=0, rotation=0)
    def request(self):
        self.result = self.husky.command_request()
        self.value = ""
        for i in range(1):
            if self.result[i][4] == 10:
                self.result[i][4] = 0
            elif self.result[i][4] == 0:
                self.result[i][4] = "?"
            self.value += str(self.result[i][4])
        return self.value

if __name__ == "__main__":
    protocol()

# while True:
#     result = husky.command_request()
#     value = ""
#     for i in range(1):
#         if result[i][4] == 10:
#             result[i][4] = 0
#         elif result[i][4] == 0:
#             result[i][4] = "?"
#         value += str(result[i][4])
#     print(value)
#     if int(value) == 1:
#         display.fill(st7789.BLACK)
#         print("Mr.Bean")
#         display.text(font2, "Mr.Bean", 10, 100,st7789.GREEN)
#         time.sleep(1)
#         print(" ")
#     if int(value) == 2:
#         display.fill(st7789.BLACK)
#         print("Champak Chacha")
#         display.text(font2, "Champak Chacha", 10, 100,st7789.YELLOW)
#         time.sleep(1)
#         print(" ")
#     if int(value) == 3:
#         display.fill(st7789.BLACK)
#         print("Jethiya")
#         display.text(font2, "Jethiya", 10, 100,st7789.BLUE)
#         time.sleep(1)
#         print(" ")