import streamlit as st
import asyncio
import httpx
import time
import json
from datetime import datetime

st.set_page_config(page_title="🤖 A2A Orchestrator", layout="wide")

# Session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# Header
st.markdown("# 🤖 A2A Multi-Agent Orchestrator")
st.markdown("*Intelligent routing • Multi-step planning • Real-time execution*")

# Sidebar - Status & Control
with st.sidebar:
    st.markdown("## ⚙️ System Control")
    
    def check_backend():
        try:
            httpx.get("http://127.0.0.1:9000/.well-known/com.example.a2a.agent", timeout=2)
            return True
        except:
            return False
    
    if st.button("🔄 Check Status"):
        if check_backend():
            st.success("✅ Backend Ready!")
        else:
            st.error("❌ Backend Not Running")
    
    st.markdown("**Setup Instructions:**")
    st.code("""
# Terminal 1: Start Backend
python streamlit_backend.py

# Terminal 2: Start Streamlit
streamlit run streamlit_app.py
    """, language="bash")

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Query", "📊 Agents", "📚 History"])

# Tab 1: Query
with tab1:
    st.markdown("### Ask the Orchestrator")
    
    query = st.text_area(
        "Enter your query:",
        height=120,
        placeholder="e.g., What is the weather in London?\nor\nResearch quantum computing and write a summary."
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        submit = st.button("🚀 Send Query", type="primary", use_container_width=True)
    with col2:
        if st.button("📝 Example", use_container_width=True):
            st.session_state.example = True
    
    if submit and query:
        with st.spinner("⏳ Processing..."):
            try:
                payload = {
                    "jsonrpc": "2.0",
                    "id": f"req_{int(time.time()*1000)}",
                    "method": "tasks/send",
                    "params": {
                        "id": f"task_{int(time.time()*1000)}",
                        "message": {"role": "user", "parts": [{"text": {"text": query}}]},
                    },
                }
                
                response = httpx.post("http://127.0.0.1:9000/", json=payload, timeout=120)
                data = response.json()
                
                # Extract response
                result = "Unable to parse response"
                try:
                    result = data["result"]["artifacts"][0]["parts"][0]["text"]["text"]
                except:
                    try:
                        result = data["result"]["status"]["message"]["parts"][0]["text"]["text"]
                    except:
                        result = str(data)
                
                # Store in history
                st.session_state.chat_log.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "query": query,
                    "response": result
                })
                
                st.markdown("---")
                st.markdown("### 📤 Response")
                st.markdown(f"```\n{result}\n```")
                
                st.download_button(
                    "📥 Download",
                    result,
                    file_name=f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Tab 2: Agents
with tab2:
    st.markdown("### 📊 Available Agents")
    
    agents = [
        ("🔬 Research Agent", 9001, "Factual questions, explanations"),
        ("🧮 Math Agent", 9002, "Calculations, statistics"),
        ("✍️ Creative Writer", 9003, "Poems, stories, emails"),
        ("📄 Summary Agent", 9004, "Text summarization"),
        ("🛠️ Tool Agent", 9005, "Metal prices, data storage"),
        ("🗄️ DB Agent", 9006, "Database queries"),
        ("🌤️ Weather Agent", 9007, "Live weather"),
    ]
    
    cols = st.columns(2)
    for i, (name, port, desc) in enumerate(agents):
        with cols[i % 2]:
            st.markdown(f"**{name}**")
            st.caption(f"Port {port}")
            st.write(desc)

# Tab 3: History
with tab3:
    st.markdown("### 📚 Query History")
    
    if st.session_state.chat_log:
        st.metric("Total Queries", len(st.session_state.chat_log))
        
        for i, log in enumerate(reversed(st.session_state.chat_log), 1):
            with st.expander(f"{log['timestamp']} — {log['query'][:40]}..."):
                st.markdown("**Query:**")
                st.code(log['query'])
                st.markdown("**Response:**")
                st.code(log['response'][:500])
        
        # Export
        if st.button("📥 Export as JSON"):
            st.download_button(
                "Download JSON",
                json.dumps(st.session_state.chat_log, indent=2),
                file_name=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
    else:
        st.info("📭 No queries yet")
