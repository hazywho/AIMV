import pyfirmata2
import time

board = pyfirmata2.ArduinoNano('/dev/ttyACM0')
servo_5 = board.get_pin('d:11:s')
# board.digital[3].write(True)
# time.sleep(5)
servo_5.write(80)
time.sleep(0.5)
servo_5.write(10)
time.sleep(0.5)
servo_5.write(80)
time.sleep(0.5)
servo_5.write(10)
time.sleep(0.5)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
servo_5.write(80)
time.sleep(0.5)
servo_5.write(10)
time.sleep(0.5)
time.sleep(1)

board.digital[10].write(True)

time.sleep(1)
board.digital[8].write(True)
time.sleep(1)
board.digital[6].write(True)
time.sleep(1)
board.digital[4].write(True)
time.sleep(1)
board.exit()