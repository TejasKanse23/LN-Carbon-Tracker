import streamlit as st
import time
from utils.chatbot import initialize_gemini, get_chat_response
from utils.theme import inject_custom_css, page_header

def show(df, lane_df):
    inject_custom_css()
    page_header("🤖", "Carbon Intelligence Assistant",
                "Ask the AI about your emissions, inefficiencies, and decarbonization strategies.")

    model = initialize_gemini()

    if not model:
        st.markdown("""
        <div style="background:rgba(239,68,68,0.10);border:1px solid rgba(239,68,68,0.30);
                    border-radius:12px;padding:1.25rem 1.5rem;margin:1rem 0;">
            <div style="font-weight:700;color:#f87171;font-size:1rem;margin-bottom:0.4rem;">
                ⚠️ API Key Not Configured
            </div>
            <div style="color:#94a3b8;font-size:0.9rem;">
                Please set <code style="background:rgba(239,68,68,0.15);padding:0.15rem 0.4rem;
                border-radius:4px;color:#fca5a5;">GEMINI_API_KEY</code> in your
                <code style="background:rgba(239,68,68,0.15);padding:0.15rem 0.4rem;
                border-radius:4px;color:#fca5a5;">.env</code> file to activate the AI assistant.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Session State ──────────────────────────────────────────
    if "chats" not in st.session_state:
        st.session_state.chats = {
            "chat_1": {
                "title": "Initial Chat",
                "messages": [{
                    "role": "assistant",
                    "content": (
                        "👋 Hey there! I'm your **Carbon Intelligence Agent**.\n\n"
                        "I can analyze your freight emissions data, identify high-impact lanes, "
                        "and help plan your decarbonization roadmap.\n\n"
                        "**How can I help you today?**"
                    )
                }]
            }
        }
        st.session_state.current_chat_id = "chat_1"
        st.session_state.chat_counter    = 1

    # ── Sidebar: Chat History ────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="padding:0.5rem 0;margin-bottom:0.5rem;">
            <div style="font-size:0.72rem;font-weight:700;color:#10b981;
                        letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.75rem;">
                💬 Chat History
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✦ New Chat", use_container_width=True, type="primary"):
            st.session_state.chat_counter += 1
            new_id = f"chat_{st.session_state.chat_counter}"
            st.session_state.chats[new_id] = {
                "title": "New Chat",
                "messages": [{"role": "assistant",
                               "content": "👋 Hey! How can I help you with your carbon tracking today?"}]
            }
            st.session_state.current_chat_id = new_id
            st.rerun()

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        for cid, cdata in list(st.session_state.chats.items())[::-1]:
            is_active = (cid == st.session_state.current_chat_id)
            btn_type  = "primary" if is_active else "secondary"
            if st.button(f"💬 {cdata['title']}", key=f"btn_{cid}",
                         use_container_width=True, type=btn_type):
                st.session_state.current_chat_id = cid
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.72rem;font-weight:700;color:#10b981;
                    letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.75rem;">
            🛠️ Agent Capabilities
        </div>
        """, unsafe_allow_html=True)

        for cap in [
            ("🔍", "Data Archeology",    "Identify high-emission nodes"),
            ("🗺️", "Route Optimization", "Suggest efficient alternatives"),
            ("📊", "Trend Analysis",     "Month-over-month comparisons"),
            ("🌿", "Strategic Planning", "Decarbonization roadmaps"),
        ]:
            st.markdown(f"""
            <div style="display:flex;gap:0.55rem;align-items:flex-start;
                        margin-bottom:0.55rem;padding:0.55rem 0.7rem;
                        background:rgba(16,185,129,0.06);border-radius:8px;
                        border:1px solid rgba(16,185,129,0.12);">
                <span style="font-size:0.95rem;">{cap[0]}</span>
                <div>
                    <div style="font-weight:600;font-size:0.78rem;color:#f1f5f9;">{cap[1]}</div>
                    <div style="font-size:0.72rem;color:#64748b;">{cap[2]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Main Chat Area ────────────────────────────────────────
    current_chat = st.session_state.chats[st.session_state.current_chat_id]

    # ── Quick Prompts (only for fresh chats) ─────────────────
    if len(current_chat["messages"]) == 1:
        st.markdown("""
        <div style="background:rgba(59,130,246,0.07);border:1px solid rgba(59,130,246,0.20);
                    border-radius:12px;padding:1rem 1.25rem;margin-bottom:1.25rem;">
            <div style="font-weight:700;color:#93c5fd;font-size:0.85rem;margin-bottom:0.5rem;">
                💡 Quick Prompts — click to get started
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")
        prompts = [
            ("🔍", "Which 5 lanes produce the most emissions?",   "p1"),
            ("📅", "Show me a summary of total emissions by month.", "p2"),
            ("🌿", "Suggest actions to reduce our carbon footprint.", "p3"),
            ("📦", "How can we improve vehicle load utilization?",  "p4"),
        ]
        for i, (icon, text, key) in enumerate(prompts):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(f"{icon} {text}", key=key, use_container_width=True):
                    submit_message(text, model, df, lane_df, current_chat)
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

    # ── Render Messages ───────────────────────────────────────
    for msg in current_chat["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── Chat Input ────────────────────────────────────────────
    if prompt := st.chat_input("Ask about shipments, lanes, or carbon reduction strategies…"):
        submit_message(prompt, model, df, lane_df, current_chat)
        st.rerun()


def submit_message(prompt, model, df, lane_df, current_chat):
    current_chat["messages"].append({"role": "user", "content": prompt})

    if len(current_chat["messages"]) == 2:
        current_chat["title"] = (prompt[:22] + "…") if len(prompt) > 22 else prompt

    with st.status("🤖 Carbon Agent is thinking…", expanded=True) as status:
        st.write("🔍 Scanning shipment records…")
        time.sleep(0.5)
        st.write("📊 Crunching emission data…")
        time.sleep(0.5)
        st.write("💡 Synthesizing strategic insights…")
        response_text = get_chat_response(model, current_chat["messages"], df, lane_df)
        status.update(label="✅ Analysis complete!", state="complete", expanded=False)

    current_chat["messages"].append({"role": "assistant", "content": response_text})
