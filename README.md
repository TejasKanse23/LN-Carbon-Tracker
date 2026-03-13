# LN Carbon Tracker 🌱

The **LN Carbon Tracker** is a full-stack project designed to monitor, analyze, and predict carbon emissions using machine learning, a web dashboard, and an AI assistant.

The system consists of **four main services** working together:

* **Node.js Backend API** – Core data service
* **FastAPI ML Service** – Carbon emission prediction engine
* **React + Vite Frontend** – Dashboard UI
* **Streamlit AI Agent** – Conversational analytics assistant

---

# 🏗️ Project Architecture

```
LN Carbon Tracker
│
├── backend                # Node.js API + ML training
├── frontend               # React + Vite dashboard
├── carbon_tracker_agent   # AI assistant (Streamlit)
└── utils                  # Data generator and utilities
```

---

# ⚙️ Prerequisites

Make sure the following tools are installed:

* **Node.js** (v18+ recommended)
* **Python** (v3.9+)
* **npm**
* **pip**
* **Git**

---

# 🛠️ Step 1 — Initial Setup (First Time Only)

If this is your **first time running the project**, you need to generate sample data and train the ML model.

Run these commands from the **root directory**.

### Generate Dataset

```bash
python carbon_tracker_agent/utils/data_generator.py
```

### Train ML Model

```bash
python backend/src/training/train_model.py
```

This will prepare the dataset and train the prediction model used by the FastAPI service.

---

# 🚀 Step 2 — Start All Core Services

The system requires **4 services running simultaneously**.

Open **four separate terminal windows** and run the following commands.

---

# 1️⃣ Node.js Backend (Main API)

This service handles communication between the frontend and backend.

```bash
cd backend
npm install
node server.js
```

**API URL**

```
http://localhost:3000
```

---

# 2️⃣ FastAPI Service (ML Prediction Engine)

Handles **carbon emission prediction** using the trained machine learning model.

Run from the **project root directory**:

```bash
uvicorn backend.src.api.carbon_api:app --port 8000
```

**API URL**

```
http://localhost:8000
```

---

# 3️⃣ Frontend Dashboard (React + Vite)

Provides the **visual analytics dashboard**.

```bash
cd frontend
npm install
npm run dev
```

**Frontend URL**

```
http://localhost:5173
```

---

# 4️⃣ AI Agent Assistant (Streamlit)

An **interactive AI assistant** for analyzing carbon data.

```bash
cd carbon_tracker_agent
pip install -r requirements.txt
streamlit run app.py
```

**AI Assistant URL**

```
http://localhost:8501
```

*(If the port is busy, Streamlit may automatically switch to `8502`.)*

---

# 📊 System Workflow

1. **Data is generated** using the data generator script.
2. **ML model is trained** using the training pipeline.
3. **FastAPI service** loads the trained model for predictions.
4. **Node.js backend** manages API requests.
5. **React frontend** displays analytics dashboards.
6. **Streamlit AI Agent** allows conversational insights.

---

# 🧪 Development Tips

* Ensure **all four services are running simultaneously**.
* If the frontend cannot fetch data, confirm:

  * Backend is running on **port 3000**
  * FastAPI is running on **port 8000**
* Restart services after major code changes.

---

# 🛑 Common Issues

### Port Already in Use

Kill the existing process or change the port.

### Missing Dependencies

Reinstall dependencies:

```bash
npm install
pip install -r requirements.txt
```

### Model Not Found

Run the training step again:

```bash
python backend/src/training/train_model.py
```

---

# 👨‍💻 Author

Developed as part of the **LN Carbon Tracker Project** for carbon emission monitoring and AI-driven sustainability insights.

---
