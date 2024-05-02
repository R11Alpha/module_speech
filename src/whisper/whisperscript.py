#!/usr/bin/env python3

import rospy
import numpy as np
import speech_recognition as sr
import whisper
import torch
import sounddevice
import pyaudio
import wave
import sys

from queue import Queue
from time import sleep
from sys import platform
# from playsound import playsound
from std_msgs.msg import String
from os import system

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

validwakeupcalls = ["robot", "road", "roll", "robot.", "road.", "roll."]


def main(pub,pub2):
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = 1000
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a
    # point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    if 'linux' in platform:
        mic_name = 'pulse'
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
    else:
        source = sr.Microphone(sample_rate=16000)

    phrase_timeout = 3

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:

        data = audio.get_raw_data()
        data_queue.put(data)

    recorder.listen_in_background(source, record_callback, phrase_time_limit=phrase_timeout)

    print("Ready\n")

    try:
        while True:
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                # Combine audio data from queue
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()

                # Convert in-ram buffer to something the model can use directly without needing a temp file.
                # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Read the transcription.
                result = model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].lower()
                text_strip = text.strip()
                text_split = text_strip.split()

                for word in text_split:
                    if word in validwakeupcalls:
                        Command(pub,pub2)
                        result = None

                sleep(0.25)
    except KeyboardInterrupt:
        pass


def Command(pub,pub2):
    try:
        # playsound('/home/markovito/Documents/markovito_ws/src/module_speech/src/whisper/audio/play.mp3')
        # Tell the user you are now listening
        confirmation_msg = String()
        confirmation_msg.data = 'yes'
        pub2.publish(confirmation_msg)
        sleep(1)
        print('Recording...')

        with wave.open('output.wav', 'wb') as wf:
            p = pyaudio.PyAudio()
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)

            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

            for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                wf.writeframes(stream.read(CHUNK))
            # playsound('/home/markovito/Documents/markovito_ws/src/module_speech/src/whisper/audio/stop.mp3')
            print('Done')

            stream.close()
            p.terminate()
            # Tell the user that the recording is done
            finished_msg = String()
            finished_msg.data = "Ok"
            pub2.publish(finished_msg)

            result = model.transcribe("output.wav", fp16=False)
            sentence = result['text']

            #debug
            print(sentence)

            pub.publish(String(sentence))

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    # Load model from the local archive that downloaded from the web page.
    model = whisper.load_model("/home/markovito/anaconda3/envs/whisper/lib/python3.9/site-packages/whisper/small.en.pt")
    rospy.init_node('whisperscript_py')
    rate = rospy.Rate(60)
    pub = rospy.Publisher("/module_speech/whisper_output", String, queue_size=50)
    pub2 = rospy.Publisher("/pocket_listener/talk", String, queue_size=1)
    main(pub,pub2)
