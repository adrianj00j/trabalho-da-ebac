from pathlib import Path
import os
import sys


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dashboard_ecommerce.app import app  # noqa: E402


if __name__ == "__main__":
    porta = int(os.getenv("PORT", "8050"))
    modo_debug = os.getenv("DASH_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=porta, debug=modo_debug)
