import uvicorn
import getpass
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"

if not os.environ.get("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_API_KEY"] = getpass.getpass()

if __name__ == "__main__":
    try:
        uvicorn.run("app.api:app", host="localhost", port=8000, reload=False, workers=1)
    except Exception as e:
        print(f"Failed to start server: {e}")