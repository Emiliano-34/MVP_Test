import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
from dotenv import load_dotenv
from services.llm import LLMClient
from core.conversation import ConversationManager
from core.prompting import build_messages


load_dotenv()


st.set_page_config(page_title="AI Copilot MVP", page_icon="🤖")

st.title("MVP")
st.markdown("---")


if "manager" not in st.session_state:
    st.session_state.manager = ConversationManager(max_turns=10)

if "llm" not in st.session_state:
    try:
        st.session_state.llm = LLMClient()
    except Exception as e:
        st.error(f"Error crítico al iniciar LLM: {e}")
        st.stop()


with st.sidebar:
    st.header("Estado del Sistema")
    turn_count = len(st.session_state.manager.get_history())
    st.metric("Turnos en memoria", f"{turn_count}/10")
    
    if st.button("Borrar Memoria"):
        st.session_state.manager = ConversationManager(max_turns=10)
        st.rerun()

# historial
for msg in st.session_state.manager.get_history():
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Usuario
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state.manager.add_message("user", prompt)
    
    # Intent
    intent = st.session_state.manager.detect_intent(prompt)
    if intent != "chat_general":
        st.toast(f"Intent detectado: {intent}")

    # respuesta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner("Pensando..."):
                messages = build_messages(st.session_state.manager.get_history())
                full_response = st.session_state.llm.get_response(messages)
                
            message_placeholder.write(full_response)
            st.session_state.manager.add_message("assistant", full_response)
            
        except Exception as e:
            error_msg = "Error de conexión. Intenta de nuevo."
            message_placeholder.error(error_msg)
            print(f"LOG ERROR: {e}")
