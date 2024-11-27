import simpleaudio as sa

class speaker():
    
    def playAudio(self,waitDone=False,path = r"/home/hezy/Downloads/final/AIMV-main/FIRMATA+RPI/siren.wav"):
        self.f=sa.WaveObject.from_wave_file(path)
        self.play_object = self.f.play()
        self.play_object.wait_done() if waitDone else None
        
    def stopAudio(self):
        self.play_object.stop()

import time
if __name__ == "__main__":
    audioMachine = speaker()
    audioMachine.playAudio()
    print("asyncronus playing is working")
    for n in range(20):
        print(f"testing {n}") 
    time.sleep(5)
    audioMachine.stopAudio()
