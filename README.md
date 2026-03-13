Here is the complete guide to running the LN Carbon Tracker project from start to finish.

📋 Full Project Execution Guide
The project consists of multiple services that work together. To run the full ecosystem, you need to start four separate processes. I have created a detailed guide as an artifact for your reference.

running_guide.md

🛠️ Step 0: First-Time Setup (Optional)
If you haven't initialized the data or the AI model yet, run these commands from the root directory:

Generate Data: python carbon_tracker_agent/utils/data_generator.py
Train Model: python backend/src/training/train_model.py
🚀 Running the 4 Core Services
You will need 4 separate terminal windows open simultaneously:

1. Node.js Backend (Main API)
This is the central hub for data and frontend requests.

powershell
cd backend
npm install
node server.js
Access: http://localhost:3000
2. FastAPI Service (ML Prediction Engine)
This handles the heavy lifting for carbon emission calculations using the trained model.

powershell
# From the root directory
uvicorn backend.src.api.carbon_api:app --port 8000
Access: http://localhost:8000
3. Frontend Dashboard (React + Vite)
The primary visual interface.

powershell
cd frontend
npm install
npm run dev
Access: http://localhost:5173
4. AI Agent Assistant (Streamlit)
The interactive conversational agent for analysis.

powershell
cd carbon_tracker_agent
pip install -r requirements.txt
streamlit run app.py
Access: http://localhost:8501 (or 8502)
