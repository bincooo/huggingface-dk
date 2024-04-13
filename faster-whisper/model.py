from faster_whisper import WhisperModel

# Current model (default to small)
current_model = None

# Function to load model
def load_model(model):
    global current_model
    # Load the model if different size is selected
    if not current_model or current_model.model != model:
        int8 = "int8"  # Adjust path as needed for Hugging Face Spaces
        current_model = WhisperModel(model, device="auto", compute_type=int8, download_root=int8)
    return current_model

current_model = load_model("small")