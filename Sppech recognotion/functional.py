import os

import speech_recognition as sp_recog
from pydub import AudioSegment


def file_audio_recognize(file_name, language_code):
    audio_file = AudioSegment.from_mp3(file_name)
    audio_file.export(os.path.join(os.getcwd(), 'work_file.wav'), format="wav")
    r = sp_recog.Recognizer()
    harvard = sp_recog.AudioFile('work_file.wav')
    with harvard as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.record(source)
    res = r.recognize_google(audio, language=language_code)
    os.remove('work_file.wav')
    return res.lower()


def life_audio_recognize(language_code):
    r = sp_recog.Recognizer()
    mic = sp_recog.Microphone()
    with mic as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    res = r.recognize_google(audio, language=language_code)
    return res.lower()
