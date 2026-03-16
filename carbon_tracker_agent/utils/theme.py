"""
Global theme injection for the Carbon Tracker Streamlit app.
Call inject_custom_css() at the top of every page.
"""
import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* ─── Google Fonts ─────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ─── Root Variables ────────────────────────────── */
    :root {
        --bg-base:       #0a0f1e;
        --bg-card:       #111827;
        --bg-card2:      #1a2236;
        --accent:        #10b981;
        --accent2:       #06d6a0;
        --accent-blue:   #3b82f6;
        --accent-amber:  #f59e0b;
        --accent-red:    #ef4444;
        --text-primary:  #f1f5f9;
        --text-muted:    #94a3b8;
        --border:        rgba(16,185,129,0.15);
        --glow:          0 0 24px rgba(16,185,129,0.18);
        --radius:        14px;
        --radius-sm:     8px;
        --transition:    0.22s cubic-bezier(.4,0,.2,1);
    }

    /* ─── Global Reset ──────────────────────────────── */
    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-base) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* App body */
    [data-testid="stAppViewContainer"] > .main {
        background: var(--bg-base) !important;
    }

    /* Block container padding */
    .block-container {
        padding: 2rem 2.5rem 4rem !important;
        max-width: 1400px !important;
    }

    /* ─── Hide sidebar & collapse arrow completely ──── */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    button[kind="header"] {
        display: none !important;
    }

    /* ─── Top Navigation Bar ────────────────────────── */
    .ct-topbar {
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 9999;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        background: linear-gradient(90deg, #0d1526 0%, #0a0f1e 100%);
        border-bottom: 1px solid rgba(16,185,129,0.18);
        box-shadow: 0 2px 24px rgba(0,0,0,0.45);
        backdrop-filter: blur(12px);
    }

    /* Brand */
    .ct-brand {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        text-decoration: none;
    }
    .ct-brand-leaf { font-size: 1.5rem; }
    .ct-brand-name {
        font-size: 1.15rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    .ct-brand-sub {
        font-size: 0.8rem;
        font-weight: 400;
        color: #64748b;
        -webkit-text-fill-color: #64748b;
    }

    /* Nav links */
    .ct-nav {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    .ct-nav-item {
        padding: 0.4rem 0.9rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.18s ease;
        white-space: nowrap;
        user-select: none;
    }
    .ct-nav-item:hover {
        background: rgba(16,185,129,0.10);
        color: #10b981;
    }
    .ct-nav-active {
        background: rgba(16,185,129,0.15) !important;
        color: #10b981 !important;
        font-weight: 600 !important;
        border: 1px solid rgba(16,185,129,0.28) !important;
    }

    /* Push body below topbar */
    .block-container {
        padding-top: 1.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1400px !important;
    }

    /* Hide the Streamlit deploy button and hamburger menu from header */
    [data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
    }
    [data-testid="stToolbar"] { display: none !important; }


    /* ─── Headings ──────────────────────────────────── */
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em !important;
        font-weight: 700 !important;
    }
    h1 {
        font-size: 2rem !important;
        background: linear-gradient(135deg, #10b981, #3b82f6);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 0.25rem !important;
    }

    /* ─── Metric Cards ──────────────────────────────── */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: var(--glow) !important;
        transition: transform var(--transition), box-shadow var(--transition) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 0 36px rgba(16,185,129,0.28) !important;
    }
    [data-testid="stMetric"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important; left: 0 !important;
        width: 3px !important; height: 100% !important;
        background: linear-gradient(180deg, var(--accent), var(--accent-blue)) !important;
        border-radius: 3px 0 0 3px !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }

    /* ─── Top Navigation Buttons (nav pills) ────────── */
    /* Wrapper that holds the nav button row — make it look like a navbar */
    [data-testid="stHorizontalBlock"]:has(button[data-testid="baseButton-secondary"],
                                           button[data-testid="baseButton-primary"]) {
        background: transparent !important;
        gap: 4px !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
    }

    /* All nav buttons base style */
    [data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"],
    [data-testid="stHorizontalBlock"] button[data-testid="baseButton-primary"] {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #94a3b8 !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.35rem 0.1rem !important;
        width: 100% !important;
        transition: all 0.18s ease !important;
        box-shadow: none !important;
    }
    [data-testid="stHorizontalBlock"] button[data-testid="baseButton-secondary"]:hover {
        background: rgba(16,185,129,0.08) !important;
        color: #10b981 !important;
        border-color: rgba(16,185,129,0.2) !important;
    }
    /* Active (primary) nav button */
    [data-testid="stHorizontalBlock"] button[data-testid="baseButton-primary"] {
        background: rgba(16,185,129,0.15) !important;
        color: #10b981 !important;
        border-color: rgba(16,185,129,0.35) !important;
        font-weight: 700 !important;
    }

    /* ─── Buttons (general) ─────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(59,130,246,0.10)) !important;
        border: 1px solid rgba(16,185,129,0.35) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all var(--transition) !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(16,185,129,0.30), rgba(59,130,246,0.22)) !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 14px rgba(16,185,129,0.30) !important;
        transform: translateY(-1px) !important;
        color: var(--accent) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        border: none !important;
        color: #fff !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #059669, #047857) !important;
        color: #fff !important;
        box-shadow: 0 0 18px rgba(16,185,129,0.45) !important;
    }


    /* ─── Inputs / Selects ──────────────────────────── */
    .stTextInput input,
    .stSelectbox select,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] {
        background: var(--bg-card2) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput input:focus,
    div[data-baseweb="input"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(16,185,129,0.2) !important;
    }

    /* ─── Dataframe / Table ─────────────────────────── */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        overflow: hidden !important;
    }

    /* ─── Plotly Charts ─────────────────────────────── */
    .js-plotly-plot .plotly {
        background: transparent !important;
    }

    /* ─── Info / Success / Warning / Error ──────────── */
    [data-testid="stAlert"] {
        border-radius: var(--radius) !important;
        border-width: 1px !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-baseweb="notification"] {
        border-radius: var(--radius) !important;
    }

    /* ─── Expander ──────────────────────────────────── */
    [data-testid="stExpander"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--glow) !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }

    /* ─── Chat Messages ─────────────────────────────── */
    [data-testid="stChatMessage"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        margin-bottom: 0.75rem !important;
        padding: 1rem 1.25rem !important;
    }
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: rgba(59,130,246,0.08) !important;
        border-color: rgba(59,130,246,0.2) !important;
    }

    /* ─── Chat Input ────────────────────────────────── */
    [data-testid="stChatInput"] textarea {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(16,185,129,0.2) !important;
    }

    /* ─── Status Widget ─────────────────────────────── */
    [data-testid="stStatus"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }

    /* ─── Divider ───────────────────────────────────── */
    hr {
        border-color: var(--border) !important;
        margin: 1.5rem 0 !important;
    }

    /* ─── Page Subtitle helper ──────────────────────── */
    .page-subtitle {
        color: var(--text-muted);
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: -0.5rem;
        margin-bottom: 1.5rem;
    }

    /* ─── Section Header helper ─────────────────────── */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }

    /* ─── Stat Badge ────────────────────────────────── */
    .stat-badge {
        display: inline-block;
        background: rgba(16,185,129,0.15);
        color: var(--accent);
        border: 1px solid rgba(16,185,129,0.30);
        border-radius: 999px;
        padding: 0.2rem 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ─── Insight Card ──────────────────────────────── */
    .insight-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        box-shadow: var(--glow);
        transition: transform var(--transition);
    }
    .insight-card:hover { transform: translateY(-2px); }
    .insight-card.green  { border-left: 3px solid var(--accent); }
    .insight-card.blue   { border-left: 3px solid var(--accent-blue); }
    .insight-card.amber  { border-left: 3px solid var(--accent-amber); }
    .insight-card.red    { border-left: 3px solid var(--accent-red); }
    .insight-card .ic-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-muted);
        margin-bottom: 0.4rem;
    }
    .insight-card .ic-body {
        font-size: 0.92rem;
        color: var(--text-primary);
        line-height: 1.55;
    }

    /* ─── Scrollbar ─────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(16,185,129,0.3); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ─── Markdown text ─────────────────────────────── */
    p, li, label, span {
        color: var(--text-primary) !important;
    }

    /* ─── Tabs ──────────────────────────────────────── */
    [data-testid="stTabs"] [role="tab"] {
        background: transparent !important;
        color: var(--text-muted) !important;
        border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
        font-weight: 600 !important;
        transition: all var(--transition) !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom-color: var(--accent) !important;
    }

    </style>
    """, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render a styled page header."""
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:0.65rem;margin-bottom:0.3rem;">
            <span style="font-size:1.8rem;">{icon}</span>
            <h1 style="margin:0;">{title}</h1>
        </div>
        {"<p class='page-subtitle'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)


def section_header(text: str):
    """Render a styled section sub-header."""
    st.markdown(f"<div class='section-header'>{text}</div>", unsafe_allow_html=True)


def insight_card(icon: str, title: str, body: str, color: str = "green"):
    """Render a styled insight card."""
    st.markdown(f"""
    <div class="insight-card {color}">
        <div class="ic-title">{icon} {title}</div>
        <div class="ic-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)
