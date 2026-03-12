🚀 Full Project Startup Commands
This project has 3 separate services that must each run in their own terminal.

Terminal 1 — 🖥️ Frontend (React + Vite)
powershell
cd c:\Users\logis\Desktop\LN-Carbon-Tracker\frontend
npm run dev
➡️ Runs at: http://localhost:5173

Terminal 2 — ⚙️ Backend (Node.js / Express)
powershell
cd c:\Users\logis\Desktop\LN-Carbon-Tracker\backend
node server.js
➡️ Runs at: http://localhost:3000 (or whatever port is set in 

server.js
)

Terminal 3 — 🤖 AI Agent (Streamlit)
powershell
cd c:\Users\logis\Desktop\LN-Carbon-Tracker\carbon_tracker_agent
streamlit run app.py
➡️ Runs at: http://localhost:8502
