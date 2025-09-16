# run.py - entrypoint for the Flask app (Replit-friendly)
# - Ensures project root is on PYTHONPATH so `import app` always works.
# - Binds to the PORT env var used by Replit.
# - Uses DEBUG env var if provided.
import os
import sys

# Ensure the project root (directory containing run.py) is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now import the app factory
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Replit (and many hosts) expose PORT env var
    port = int(os.environ.get("PORT", 5000))
    debug_env = os.environ.get("DEBUG", "").lower()
    debug = True if debug_env in ("1", "true", "yes") else False
    # Use 0.0.0.0 so the server is reachable from the Replit public URL
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)