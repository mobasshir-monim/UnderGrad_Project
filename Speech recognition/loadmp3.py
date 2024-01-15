from pydub import AudioSegment
audio=AudioSegment.from_wav("Output.wav")

audio=audio+5
audio=audio.fade_in(2000)
audio.export("output2.mp3",format="mp3")