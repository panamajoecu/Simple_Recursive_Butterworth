from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
import csv

sound = AudioSegment.from_file("Extended_chirp.wav", format="wav")

print sound.rms
print sound.channels
print sound.duration_seconds

# get raw audio data as a bytestring
raw_data = sound._data
# get the frame rate
sample_rate = sound.frame_rate
# get amount of bytes contained in one sample
sample_size = sound.sample_width
# get channels
channels = sound.channels

raw_data = np.fromstring(raw_data, 'Int16')

cnt = 0
with open('output.csv','wb') as csvfile:
    spamwriter = csv.writer(csvfile)
    for val in raw_data:
        cnt+=1
        spamwriter.writerow([cnt, val, -val, val, -val, val, -val, val, -val])
        
plt.figure(1)
plt.title('Signal Wave...')
plt.plot(raw_data)
plt.show()
