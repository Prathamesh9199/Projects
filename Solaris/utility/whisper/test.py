import os
os.environ["PATH"] += os.pathsep + "C:/ffmpeg/bin"

# save this as transcribe.py
import whisper

model = whisper.load_model("base")
result = model.transcribe(r"data\\ENG_UK_M_PeterB.mp3")
print(result["text"])
