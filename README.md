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
   - Add some sources (Wikipedia article titles or .txt or .pdf file uploads) *Have not yet tested .docx and .doc support 
   - Query the RAG system
   - Clear the history (either by reloading or clicking the trash icon in the chat entry box)
   - Clear all sources added
