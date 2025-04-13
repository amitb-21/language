import pickle
import os

# Load the model once
MODEL_PATH = os.path.join(os.path.dirname(__file__), "segment_model.pkl")

with open(MODEL_PATH, "rb") as f:
    segment_model = pickle.load(f)

def segment_text(text: str, language: str) -> list:
    result = segment_model.predict([text])
    return result[0] if isinstance(result, list) else result
