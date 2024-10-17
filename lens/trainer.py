from huskylensPythonLibrary import HuskyLensLibrary
import time
husky = HuskyLensLibrary("I2C")
 
for i in range(1000):
    husky.command_request_learn_once(1)
    time.sleep(0.05)