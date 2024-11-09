from HLPYTHON import HuskyLensLibrary
import serial
import json

algorthimsByteID = {
    "ALGORITHM_OBJECT_TRACKING": "0100",
    "ALGORITHM_FACE_RECOGNITION": "0000",
    "ALGORITHM_OBJECT_RECOGNITION": "0200",
    "ALGORITHM_LINE_TRACKING": "0300",
    "ALGORITHM_COLOR_RECOGNITION": "0400",
    "ALGORITHM_TAG_RECOGNITION": "0500",
    "ALGORITHM_OBJECT_CLASSIFICATION": "0600",
    "ALGORITHM_QR_CODE_RECOGNTITION": "0700",
    "ALGORITHM_BARCODE_RECOGNTITION": "0800",
}
commandList = ['knock()', 
               'setCustomName() #Random String & Cords', 
               'customText() #Random String & Cords', 
               'clearText()', 
               'requestAll()', 
               'saveModelToSDCard(1)', 
               'loadModelFromSDCard(1)', 
               'savePictureToSDCard()', 
               'count()',
               'learnedObjCount()',
               'saveScreenshotToSDCard()', 
               'blocks()', 
               'arrows()', 
               'learned()', 
               'learnedBlocks()', 
               'learnedArrows()', 
               'getObjectByID(1)', 
               'getBlocksByID(1)', 
               'getArrowsByID(1)', 
               'algorthim() #Random Choice', 
               'learn(1)', 
               'forget()', 
               'frameNumber()',
               ""
            ]

class lens():
    def __init__(self,address=0x32,connectionType="I2C"):
        self.hl = HuskyLensLibrary(connectionType,"", address=address)
    
    def __str__(self):
        returnString="MENU OPTIONS:\n"
        finalStr = "".join([chr(i+97)+"). "+commandList[i].ljust(45, " ")+chr(i+1+97)+"). "+commandList[i+1]+"\n " for i in range(0, len(commandList)-1, 2)])
        return returnString+finalStr
    
    def requestChokingStatus(self,chokingID=2):
        try:
            self.hl.getObjectByID(chokingID)
            self.status=1
        except ValueError:
            self.status = 0
            
        return 0

    
if __name__ == "__main__":
    testing = lens()
    print(testing)