import sounddevice as sd
from scipy.io.wavfile import write

def record_audio():
    sd.default.device = 0
    frequency = 44100
    duration = 5

    print("Nagrywanie...")

    recording = sd.rec(int(duration * frequency), samplerate=frequency, channels=1)
    sd.wait()

    write("nagranie.wav", frequency, recording)

    print("Nagrywanie zakończone i zapisane do pliku 'nagranie.wav'")



print(sd.query_devices())
sd.default.device = 4
print(sd.query_devices())
record_audio()