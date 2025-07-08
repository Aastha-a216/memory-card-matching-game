import wave
import struct
import math

def create_beep(filename, freq=440, duration_ms=100, volume=32767):
    framerate = 44100
    num_samples = int(framerate * duration_ms / 1000)
    wav_file = wave.open(filename, 'w')
    wav_file.setparams((1, 2, framerate, num_samples, "NONE", "not compressed"))

    for i in range(num_samples):
        sample = volume * math.sin(2 * math.pi * freq * i / framerate)
        wav_file.writeframes(struct.pack('h', int(sample)))

    wav_file.close()

# Create flip sound (440Hz beep)
create_beep('flip.wav', freq=440, duration_ms=80)

# Create match sound (660Hz beep)
create_beep('match.wav', freq=660, duration_ms=150)
