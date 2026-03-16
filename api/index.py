import sys
import os

# ── Fix Python path so that 'src.*' imports resolve correctly ──────────────────
# Vercel runs from project root, but our code imports as 'from src.xxx import ...'
# We add the backend/ directory to sys.path so those imports work.
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, os.path.abspath(BACKEND_DIR))

# ── Now import the FastAPI app ─────────────────────────────────────────────────
from src.api.main import app  # noqa: E402  (import after sys.path tweak is intentional)
