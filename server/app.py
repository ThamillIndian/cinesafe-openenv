import uvicorn
import os
from cinesafe_openenv.server.app import app

def main():
    """Mandatory entry point for OpenEnv multi-mode deployment."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 7860))
    # We use a string for the app so that reload=True works if needed, 
    # and to match the standard uvicorn entry pattern.
    uvicorn.run("server.app:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
