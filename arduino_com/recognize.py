import speech_recognition as sr
from vosk import Model

r = sr.Recognizer()
r.vosk_model = Model(
    model_name="vosk-model-en-us-0.22",
    model_path="model",
    lang="en",
)


def recognize_speech(chunk=1024):
    try:
        with sr.Microphone(chunk_size=chunk) as source2:
            print("Start talking:")
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_vosk(audio2)
            text = sr.json.loads(MyText)["text"]

            return text

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")
