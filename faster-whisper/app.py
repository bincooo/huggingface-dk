import io
import gradio as gr
from faster_whisper import WhisperModel
from time import time
import logging
import json

import sio
import model as mod
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import uvicorn

app = FastAPI()
sio.server(app)
# Initialize logging
logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)
CHOICES = [
    "tiny", "tiny.en", "base", 
    "base.en", "small", "small.en", 
    "medium", "medium.en", "large-v1", 
    "large-v2", "large-v3", "large"
]

def transcribe(audio_file, model, vad):
    # Load the model if different size is selected
    current_model = mod.load_model(model)

    start = time()
    print("audio_file: %s" % audio_file)
    # test BinaryIO
    # with open(audio_file, "rb") as f:
    #     fd = f.read()
    # binIO = io.BytesIO(fd)
    # print(f"Time load audio_file: {time() - start}")
    
    segments, info = current_model.transcribe(
        # binIO,
        audio_file,
        vad_filter=vad,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    # Prepare JSON output
    transcript = [{"start": segment.start, "end": segment.end, "text": segment.text} for segment in segments]
    print(f"Time Taken to transcribe: {time() - start}")
    output = {
        "language": info.language,
        "language_probability": info.language_probability,
        "transcript": transcript
    }

    return json.dumps(output, indent=4)

# Define Gradio interface
iface = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(type="filepath", label="Upload MP3 Audio File"),
        gr.Dropdown(choices=CHOICES, value="small", label="Model"),
        gr.Checkbox(label="vad filter stream", value=True)
    ],
    outputs=gr.JSON(label="Transcription with Timestamps"),
    title="Whisper Transcription Service",
    description="Upload an MP3 audio file to transcribe. Select the model. The output includes the transcription with timestamps.",
    concurrency_limit=2
)

# Launch the app
if __name__ == "__main__":
    #iface.launch()
    app = gr.mount_gradio_app(app, iface, path="/")
    uvicorn.run(app, host="0.0.0.0", port=7860)