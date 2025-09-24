import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("LANGSMITH_API_KEY"): #Trace only if we have an API key
    os.environ["LANGSMITH_TRACING"] = "true"

if __name__ == "__main__":
    try:
        uvicorn.run("app.api:app", host="localhost", port=8000, reload=True, workers=1)
    except Exception as e:
        print(f"Failed to start server: {e}")