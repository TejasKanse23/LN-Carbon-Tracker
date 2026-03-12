import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd

st.set_page_config(
    page_title="Carbon Tracker Agent",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize data and session state
from utils.data_generator import generate_mock_data

@st.cache_data
def load_data():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
    
    # Load the new 5000 records datasets provided by the user
    df = pd.read_csv("data/5000 lanes shipments.csv")
    lane_df = pd.read_csv("data/Lanes Summary (5000).csv")
    
    # Standardize column types
    df['date'] = pd.to_datetime(df['date'])
    
    return df, lane_df

df, lane_df = load_data()

# Navigation
st.sidebar.title("🌱 Carbon Intelligence")
st.sidebar.markdown("*AI-powered Carbon Tracker for Road Freight*")

pages = {
    "📊 Dashboard": "views/overview.py",
    "🚚 Shipments": "views/shipments.py",
    "🛣️ Lanes": "views/lanes.py",
    "🤖 AI Assistant": "views/assistant.py",
    "📖 Methodology": "views/methodology.py"
}

st.sidebar.markdown("---")
selection = st.sidebar.radio("Navigation", list(pages.keys()))

st.sidebar.markdown("---")
st.sidebar.info(
    "**Carbon Tracker Agent**\n\n"
    "Decision support tool for freight sustainability."
)

if selection == "📊 Dashboard":
    from views import overview
    overview.show(df, lane_df)
elif selection == "🚚 Shipments":
    from views import shipments
    shipments.show(df)
elif selection == "🛣️ Lanes":
    from views import lanes
    lanes.show(lane_df)
elif selection == "🤖 AI Assistant":
    from views import assistant
    assistant.show(df, lane_df)
elif selection == "📖 Methodology":
    from views import methodology
    methodology.show()
