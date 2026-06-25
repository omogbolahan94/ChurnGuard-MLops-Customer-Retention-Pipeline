import joblib
from Backend.config import MODEL_PATH


# LOADING THE SAVED ARTIFACT
_artifact = joblib.load(MODEL_PATH)

MODEL     = _artifact["model"]
PREPROC   = _artifact["preprocessor"]
THRESHOLD = _artifact["threshold"]
METRICS   = _artifact["metrics"]
