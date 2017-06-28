import sounddevice as sd
import soundfile as sf
import time
import os
from transcribe import Transcribe
import sys


class Speech:
    def __init__(self, duration=2, language='cmn-Hant-TW'):
        self.duration = duration
        self.language = language
        self.transcripts_list = None
        self.process()

    def process(self):
        device_info = sd.query_devices(sd.default.device, 'input')
        mysamplerate = device_info['default_samplerate']

        voiceFile = os.path.join(os.getcwd(), "transcript.wav")
        if os.path.isfile(voiceFile):
            os.remove(voiceFile)

        myrecord = sd.rec(int(self.duration * 16000), samplerate=16000, channels=1)
        sd.wait()
        sf.write("transcript.wav", myrecord, 16000)
        trans = Transcribe(voiceFile, self.language)
        self.transcripts_list = trans.transcripts_list
