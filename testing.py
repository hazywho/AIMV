from pydub import AudioSegment
import sys
sys.set_int_max_str_digits(0)
sound = AudioSegment.from_wav(r"C:\Users\zanyi\Documents\GitHub\AIMV\pop.wav")

# sound._data is a bytestring
raw_data = sound._data
integer = int.from_bytes(raw_data, byteorder='little')
with open(r"new.txt","w") as f:
    f.write(str(integer))