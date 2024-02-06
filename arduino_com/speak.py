import pyttsx3

engine = pyttsx3.init(debug=True)


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine.say(command)
    engine.runAndWait()
