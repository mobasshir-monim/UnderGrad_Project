import pyaudio
import json
from vosk import Model, KaldiRecognizer
from threading import Thread
from queue import Queue

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

p.terminate()

CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 3
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

messages = Queue()
recordings = Queue()

from speak import SpeakText

# from send_data import send_coeffs


def record_microphone(
    element,
    chunk=1024,
):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate=FRAME_RATE,
        input=True,
        input_device_index=1,
        frames_per_buffer=chunk,
    )

    frames = []

    parent = element.parent.parent.parent
    output = parent.output
    parent.record_button.disabled = True
    parent.stop_button.disabled = False

    while not messages.empty():
        data = stream.read(chunk)
        frames.append(data)
        if len(frames) >= (FRAME_RATE * RECORD_SECONDS) / chunk:
            # recordings.put(frames.copy())
            rec.AcceptWaveform(b"".join(frames.copy()))
            result = rec.Result()
            text = json.loads(result)["text"]
            print(text)
            frames = []

            prev = output.text
            output.text = f"{prev} {text}"
            SpeakText(text)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("stream closed...")


model = Model(model_name="vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)


def start_recording(element):
    messages.put(True)
    # with output:
    print("Starting....")
    global record
    record = Thread(
        target=record_microphone,
        args=(
            element,
            1024,
        ),
    )
    record.start()


def stop_recording(element):
    # with output:
    parent = element.parent.parent.parent
    parent.record_button.disabled = False
    parent.stop_button.disabled = True
    messages.get()
    record.join()
    print("Stopped....")


import kivy

kivy.require("2.3.0")  # replace with your current kivy version !

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen


def print_shit(dd):
    print("shit...")
    print(dd.parent.parent.parent.output.text)


class SpeechRecognitionScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SpeechRecognitionScreen, self).__init__(**kwargs)
        self.box = MDBoxLayout(
            orientation="vertical",
            spacing=1,
            size_hint_y=1,
            pos_hint={"center_y": 1.1},
            padding=10,
        )
        self.box.add_widget(
            MDLabel(
                font_style="H4",
                text="Speech Recognition",
                halign="center",
                size_hint_y=None,
                pos_hint={"center_y": 0.90},
                text_color="red",
            )
        )
        self.grid = MDGridLayout(
            cols=2,
            spacing=20,
            pos_hint={"center_x": 0.45, "center_y": 0.85},
            size_hint=(None, None),
        )

        self.record_button = MDRaisedButton(
            id="record",
            text="Record",
            on_release=start_recording,
        )
        self.stop_button = MDRaisedButton(
            id="stop",
            text="Stop",
            on_release=stop_recording,
            disabled=True,
        )
        self.grid.add_widget(self.record_button)
        self.grid.add_widget(self.stop_button)

        self.box.add_widget(self.grid)

        self.output = MDLabel(
            id="output",
            font_style="Body1",
            text="Output:",
            halign="center",
            size_hint_y=None,
            pos_hint={"center_y": 0.95},
            text_color="red",
        )

        self.box.add_widget(self.output)

        self.add_widget(self.box)


class MyApp(MDApp):
    def build(self):
        self.title = "Visual Vocal"
        return SpeechRecognitionScreen()


if __name__ == "__main__":
    MyApp().run()
