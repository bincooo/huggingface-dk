from typing import BinaryIO
from time import time
import model as mod
import socketio
import json
import io

class PrefixNamespace(socketio.AsyncNamespace):
    def __init__(self, sio, prefix):
        super().__init__(prefix)
        self.sio = sio
        self.model = "small"
        self.vad = True

    def on_connect(self, sid, environ):
        print("connect ", sid)

    async def on_message(self, sid, data):
        print("message", data)
        try:
            obj = json.loads(data)
            if "model" in obj:
                self.model = obj["model"]
            if "vad" in obj:
                self.vad = obj["vad"]
        except Exception as e:
            print("An exception occurred: ", e)
            await self.sio.emit("error", "An exception occurred.")

    async def on_raw_message(self, sid, data, uin):
        print("raw_message", sid)
        if not isinstance(data, bytes):
            print("An exception occurred: not bytes")
            await self.sio.emit("error", "An exception occurred: not bytes.")
            return

        res = transcribe(io.BytesIO(data), self.model, self.vad, uin)
        await self.sio.emit("response", res)

    def on_disconnect(self, sid):
        print("disconnect ", sid)

def server(app):
    sio = socketio.AsyncServer(
        async_mode='asgi',
        cors_allowed_origins="*",
    )

    sio.register_namespace(PrefixNamespace(sio, "/"))
    sio_asgi_app = socketio.ASGIApp(
        socketio_server=sio,
        other_asgi_app=app
    )

    app.add_route("/socket.io/", route=sio_asgi_app, methods=["GET", "POST"])
    app.add_websocket_route("/socket.io/", sio_asgi_app)
    return sio

def transcribe(audio: BinaryIO, model: str, vad: bool, uin: str):
    # Load the model if different size is selected
    current_model = mod.load_model(model)

    start = time()    
    segments, info = current_model.transcribe(
        audio,
        vad_filter=vad,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    # Prepare JSON output
    transcript = [{"start": segment.start, "end": segment.end, "text": segment.text} for segment in segments]
    print(f"Time Taken to transcribe: {time() - start}")
    output = {
        "uin": uin,
        "language": info.language,
        "language_probability": info.language_probability,
        "transcript": transcript
    }

    return json.dumps(output, indent=4)
