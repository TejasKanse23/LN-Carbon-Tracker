import streamlit as st
from utils.chatbot import initialize_gemini, get_chat_response

def show(df, lane_df):
    st.title("🤖 Carbon Intelligence Assistant")
    st.markdown("Ask the AI about your emissions, inefficiencies, and decarbonization strategies.")
    
    model = initialize_gemini()
    
    if not model:
        st.error("⚠️ GEMINI_API_KEY is not set or valid. Please check your .env file.")
        st.info("Add GEMINI_API_KEY=your_key to your .env file in the root directory.")
        return
        
    # State initialization for multi-chat support
    if "chats" not in st.session_state:
        st.session_state.chats = {
            "chat_1": {
                "title": "New Chat",
                "messages": [{"role": "assistant", "content": "Hi! Hello, how are you doing today?"}]
            }
        }
        st.session_state.current_chat_id = "chat_1"
        st.session_state.chat_counter = 1

    # Use the Sidebar exclusively for the ChatGPT-style History
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 💬 Chat History")
        
        # Mimicking the "New Chat" button at the top of the history list
        if st.button("📝 New chat", use_container_width=True, type="primary"):
            st.session_state.chat_counter += 1
            new_id = f"chat_{st.session_state.chat_counter}"
            st.session_state.chats[new_id] = {
                "title": f"New Chat",
                "messages": [{"role": "assistant", "content": "Hi! Hello, how are you doing today?"}]
            }
            st.session_state.current_chat_id = new_id
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Recents**")
        
        for cid, cdata in list(st.session_state.chats.items())[::-1]:
            # Highlight the active chat visually
            is_active = (cid == st.session_state.current_chat_id)
            btn_type = "primary" if is_active else "secondary"
            # Show the chat title like ChatGPT history
            title = cdata['title']
            if st.button(f"💬 {title}", key=f"btn_{cid}", use_container_width=True, type=btn_type):
                st.session_state.current_chat_id = cid
                st.rerun()

    # The Main Area is purely for the ChatGPT messaging interface
    current_chat = st.session_state.chats[st.session_state.current_chat_id]

    # Welcome / Quick actions if it's a completely new chat
    if len(current_chat["messages"]) == 1:
        st.info("💡 **Welcome!** I am your General Assistant. You can chat with me normally, or ask me specialized questions about your freight emissions.")
        st.markdown("##### Quick Analytics Prompts")
        prompts = [
            "Which route produces the most emissions?",
            "Suggest actions to reduce our carbon footprint."
        ]
        cols = st.columns(2)
        for i, p in enumerate(prompts):
            if cols[i].button(p, key=f"prompt_{i}"):
                submit_message(p, model, df, lane_df, current_chat)
                st.rerun()
        st.markdown("---")

    # Render all chat messages cleanly
    for msg in current_chat["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
        
    # Bottom chat input bar
    if prompt := st.chat_input("Ask a question (e.g., 'hello', or 'what is the worst lane?')..."):
        submit_message(prompt, model, df, lane_df, current_chat)
        st.rerun()

def submit_message(prompt, model, df, lane_df, current_chat):
    current_chat["messages"].append({"role": "user", "content": prompt})
    
    # Auto-title the chat based on the first user message
    if len(current_chat["messages"]) == 2:
        current_chat["title"] = prompt[:20] + "..." if len(prompt) > 20 else prompt
        
    with st.spinner("Processing..."):
        response_text = get_chat_response(model, current_chat["messages"], df, lane_df)
    current_chat["messages"].append({"role": "assistant", "content": response_text})
