import pytest
from core.conversation import ConversationManager
from core.prompting import build_messages

# TESTS DE CONVERSACIÓN 

def test_add_message():
    #Prueba que se guarden mensajes en el historial
    cm = ConversationManager()
    cm.add_message("user", "Hola")
    assert len(cm.get_history()) == 1
    assert cm.get_history()[0]["content"] == "Hola"

def test_memory_limit():
    #Prueba el limite de memoria
    cm = ConversationManager(max_turns=2)
    cm.add_message("user", "1")
    cm.add_message("assistant", "2")
    cm.add_message("user", "3") # Esto debería borrar el "1"
    
    hist = cm.get_history()
    assert len(hist) == 2
    assert hist[0]["content"] == "2" # El más antiguo ahora es el 2

def test_intent_detection():
    #Prueba comandos especiales
    cm = ConversationManager()
    assert cm.detect_intent("/nota Comprar pan") == "guardar_nota"
    assert cm.detect_intent("Hola mundo") == "chat_general"

# TEST PROMPTING

def test_system_prompt_structure():
    #Prueba que el system prompt esté siempre al inicio
    msgs = build_messages([])
    assert msgs[0]["role"] == "system"
    assert "AI Copilot" in msgs[0]["content"]

def test_history_integration():
    #prueba que combine system prompt JUNTO al historial
    history = [{"role": "user", "content": "Hola"}]
    msgs = build_messages(history)
    assert len(msgs) == 2 # 1 system + 1 user
    assert msgs[1]["content"] == "Hola"

def test_prompt_integrity():
    #Verifica que no se pierdan datos en el prompt
    history = [{"role": "user", "content": "Test"}]
    msgs = build_messages(history)
    assert isinstance(msgs, list)
    assert msgs[0]["role"] == "system"
