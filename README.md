NOTE: Currently commiting things to work with deployment, last working commit is https://github.com/ivanquon/AI-projects/commit/3c19436953d4ab5a87cc5466769e37c5fe82efbb, will fix read.me later after working deployment

Running the RAG application locally,

1. Postgres Database
   - Log into PostgresSQL and create a database
   - Install pgvector https://github.com/pgvector/pgvector
   - Move to backend
     ```cd basic-app/backend```
   - Create a .env file and add the following environment variables with corresponding values (Values given are samples, they likely wont work)
     - POSTGRES_USER="username"
     - POSTGRES_PASSWORD="password"
     - POSTGRES_DB="name"
     - POSTGRES_HOST="localhost"
     - POSTGRES_PORT="5432"

2. Backend
   - Move to backend
     ```cd basic-app/backend```
   - Create a python virtual environment using
     ```
     python -m venv venv
     source venv/bin/activate
     ```
   - Install python dependencies
     ```
     pip install -r requirements.txt
     ```
   - Add to .env file with the following
     - LANGSMITH_API_KEY="YOUR_API_KEY" (optional for logging and tracing
     - GOOGLE_API_KEY="YOUR_API_KEY" (required for gemini api llm, a basic key is free https://aistudio.google.com/app/api-keys)
   - Run main.py
     ```
     python main.py
     ```
   - Note: I had to install https://github.com/tesseract-ocr/tesseract for pdf support, likely will also need to install for pdf upload functionality to work properly
3. Frontend
   - Move to frontend
     ```cd basic-app/frontend```
   - Install dependencies
     ```
     npm install
     ```
   - Run the frontend and access from http://localhost:5173/
     ```
     npm run dev
     ```
4. Usage
   - Add some sources (Wikipedia article titles or .txt file uploads, .pdf partially works but it is WIP for better preprocessing) *Have not yet tested .docx and .doc support 
   - Query the RAG system
   - Clear the history (either by reloading or clicking the trash icon in the chat entry box)
   - Clear all sources added
