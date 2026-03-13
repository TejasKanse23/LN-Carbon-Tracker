🌱 LN Carbon Tracker

A full-stack carbon emissions tracking platform with an AI assistant that helps users analyze and understand their carbon footprint.

The project consists of three services:

🖥️ Frontend – React + Vite dashboard

⚙️ Backend – Node.js / Express API

🤖 AI Agent – Streamlit-based AI assistant

🏗️ Project Architecture
LN-Carbon-Tracker
│
├── frontend/              # React + Vite frontend
│
├── backend/               # Node.js / Express API
│
├── carbon_tracker_agent/  # Streamlit AI assistant
│
└── README.md
⚙️ Requirements

Make sure you have installed:

Node.js (v18+ recommended)

npm

Python 3.9+

pip

Streamlit

🚀 Running the Project

The system requires 3 separate terminals.

🖥️ Terminal 1 — Frontend (React + Vite)

Navigate to the frontend directory and start the dev server.

cd c:\Users\logis\Desktop\LN-Carbon-Tracker\frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173
⚙️ Terminal 2 — Backend (Node.js / Express)

Navigate to the backend folder and start the API server.

cd c:\Users\logis\Desktop\LN-Carbon-Tracker\backend
npm install
node server.js

Backend runs at:

http://localhost:3000

(Port may vary depending on configuration in server.js)

🤖 Terminal 3 — AI Agent (Streamlit)

Navigate to the AI agent folder and launch the Streamlit app.

cd c:\Users\logis\Desktop\LN-Carbon-Tracker\carbon_tracker_agent
pip install -r requirements.txt
streamlit run app.py

AI Agent runs at:

http://localhost:8502
🌍 Features

📊 Carbon emissions tracking dashboard

📈 Data visualization of carbon footprint

🤖 AI-powered sustainability assistant

⚡ Real-time interaction between frontend and backend

🌱 Environmental insights and recommendations

🔌 Services Overview
Service	Tech Stack	Port
Frontend	React + Vite	5173
Backend	Node.js + Express	3000
AI Agent	Python + Streamlit	8502
🧪 Development Notes

All services must run simultaneously

Ensure the backend API is running before using the frontend

The AI agent communicates with the backend for analysis

📌 Future Improvements

Carbon emission prediction models

User authentication

Database integration

Cloud deployment

Advanced AI analytics
