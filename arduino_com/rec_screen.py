from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from threading import Thread
import pyaudio
from vosk import Model, KaldiRecognizer

import store as rec_store
from recognize import recognize_speech
from speak import SpeakText
from send_data import send_coeffs
from collections import defaultdict
from alphabets_data import alphabets_data


def get_default():
    return [0, 0, 0, 0, 0, 0]


short_data = {
    "hello": "hl",
    "good morning": "gm",
    "good afternoon": "ga",
    "good evening": "ge",
    "how are you": "hay",
    "im doing well": "imdw",
    "thank you": "ty",
    "youre welcome": "yw",
    "nice to meet you": "ntmu",
    "please": "p",
    "excuse me": "em",
    "i love you": "ily",
    "goodbye": "gb",
    "see you later": "syl",
    "have a nice day": "hnd",
    "yes": "y",
    "no": "n",
    "maybe": "m",
    "i understand": "iu",
    "sorry": "s",
    "thank you for your time": "tyft",
    "what is your name": "wyn",
    "my name is": "mni",
    "how can i help you": "hciu",
    "i need help": "ihn",
    "excuse me can you help me": "eccy",
    "do you speak sign language": "dysl",
    "yes i do": "yi",
    "no i dont": "ni",
    "can you write that down": "cywd",
    "please repeat that": "prt",
    "i apologize": "ia",
    "can you speak slower": "cs",
    "can you speak louder": "cl",
    "thank you for your patience": "tyfp",
    "i hope you have a wonderful day": "ihwwd",
}

numeric_data = {
    "zero": [0, 0, 0, 0, 0, 0],
    "one": [1, 0, 0, 0, 0, 0],
    "two": [0, 1, 0, 0, 0, 0],
    "three": [0, 0, 1, 0, 0, 0],
    "four": [0, 0, 0, 1, 0, 0],
    "five": [0, 0, 0, 0, 1, 0],
    "six": [1, 0, 0, 0, 1, 0],
    "seven": [0, 1, 0, 0, 1, 0],
    "eight": [0, 0, 1, 0, 1, 0],
    "nine": [0, 0, 0, 1, 1, 0],
}

final_data = defaultdict(
    get_default,
    {
        **numeric_data,
        **alphabets_data("alphabets.csv"),
        "fuck": [0, 1, 0, 0, 0, 0],
    },
)


def recognize_dummy(text: str):
    return final_data[text.strip()]


CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 3
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

model = Model(model_name="vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, FRAME_RATE)
rec.SetWords(True)
rec.SetNLSML(True)


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
            on_release=self.start_recording,
        )
        self.stop_button = MDRaisedButton(
            id="stop",
            text="Stop",
            on_release=self.stop_recording,
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

    def start_recording(self, _el):
        rec_store.start()
        print("Starting...")
        self.record_button.disabled = True
        self.stop_button.disabled = False
        self.record = Thread(
            target=self.record_speech,
            args=(1024,),
        )
        self.record.start()

    def stop_recording(self, el):
        self.record_button.disabled = False
        self.stop_button.disabled = True
        rec_store.end()
        self.record.join()
        print("Stopped...")

    def record_speech(self, chunk=512):
        while rec_store.is_recording():
            text = recognize_speech(chunk)
            prev = self.output.text
            self.output.text = f"{prev} {text}"
            self.send_data(text)

    def send_data(self, text: str):
        print(text)
        short = short_data.get(text)
        if short is None:
            for split_text in str(text).split(" "):
                split_text = split_text.lower()
                send_coeffs(recognize_dummy(split_text))
                # SpeakText(split_text)
        else:
            for split_text in [*short]:
                split_text = split_text.lower()
                send_coeffs(recognize_dummy(split_text))
                # SpeakText(split_text)
