import kivy

kivy.require("2.3.0")  # replace with your current kivy version !

from kivymd.app import MDApp
from rec_screen import SpeechRecognitionScreen


class MyApp(MDApp):
    def build(self):
        self.title = "Visual Vocal"
        return SpeechRecognitionScreen()


if __name__ == "__main__":
    MyApp().run()
