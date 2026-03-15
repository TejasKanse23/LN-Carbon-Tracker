import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd

st.set_page_config(
    page_title="CarbonTrack – by LogisticsNow",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Inject global theme ───────────────────────────────────────────────────
from utils.theme import inject_custom_css
inject_custom_css()

# ─── Load environment variables ────────────────────────────────────────────
load_dotenv()

# ─── Data loading ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)
    df = pd.read_csv("data/carbon_tracker_shipments.csv")
    lane_df = pd.read_csv("data/carbon_tracker_lane_summary.csv")
    
    df['date'] = pd.to_datetime(df['date'])
    return df, lane_df

df, lane_df = load_data()

# ─── Session state for active page ─────────────────────────────────────────
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

NAV_PAGES = [
    ("📊", "Dashboard"),
    ("🚚", "Shipments"),
    ("🛣️", "Lanes"),
    ("📄", "Lane Report"),
    ("🤖", "AI Assistant"),
    ("🔮", "AI Forecast"),
    ("📦", "Consolidation Agent"),
    ("📖", "Methodology"),
]

# ─── Brand header bar ──────────────────────────────────────────────────────
st.markdown("""
<div class="ct-topbar">
    <div class="ct-brand">
        <span class="ct-brand-leaf">🌿</span>
        <span class="ct-brand-name">CarbonTrack</span>
        <span class="ct-brand-sub">&nbsp;– by LogisticsNow</span>
    </div>
</div>
<div style="height:64px;"></div>
""", unsafe_allow_html=True)

# ─── Nav buttons row (real Streamlit buttons, CSS-styled as nav pills) ─────
cols = st.columns(len(NAV_PAGES))
for col, (icon, label) in zip(cols, NAV_PAGES):
    is_active = st.session_state.active_page == label
    # Inject per-button CSS class via a wrapper key
    with col:
        # Use a unique key; active state adds extra class via CSS trick below
        clicked = st.button(
            f"{icon} {label}",
            key=f"nav__{label}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        )
        if clicked:
            st.session_state.active_page = label
            st.rerun()

st.markdown("<hr style='margin:0 0 1.5rem 0; border-color:rgba(16,185,129,0.15);'>", unsafe_allow_html=True)

# ─── Page routing ──────────────────────────────────────────────────────────
page = st.session_state.active_page

if page == "Dashboard":
    from views import overview
    overview.show(df, lane_df)
elif page == "Shipments":
    from views import shipments
    shipments.show(df)
elif page == "Lanes":
    from views import lanes
    lanes.show(lane_df)
elif page == "Lane Report":
    from views import report_generator
    report_generator.show()
elif page == "AI Assistant":
    from views import assistant
    assistant.show(df, lane_df)
elif page == "AI Forecast":
    from views import forecasting
    forecasting.show(df)
elif page == "Consolidation Agent":
    from views import consolidation
    consolidation.show(df)
elif page == "Methodology":
    from views import methodology
    methodology.show()
