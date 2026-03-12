# LN Carbon Tracker

A full-stack hackathon project to calculate carbon emissions based on transportation.

## Project Overview
LN Carbon Tracker provides a simple web interface where users can input distance and vehicle type (car, van, or truck) to estimate their carbon emission per trip.

## Tech Stack
- **Frontend**: React (with Vite), JavaScript, and modern CSS
- **Backend**: Python, FastAPI
- **REST API architecture**

## Repository Structure
```text
LN-Carbon-Tracker/
├── frontend/             # React application with Vite
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
└── backend/              # Python FastAPI application
    ├── app.py
    ├── requirements.txt
    ├── routes/
    └── services/
```

## Setup Instructions

### 1. Run the Backend

1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
   The backend will start at `http://localhost:8000`. You can check the health status by visiting `http://localhost:8000/health`.

### 2. Run the Frontend

1. Open another terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`. Open it in your browser to see the Dashboard and calculate carbon emissions!
