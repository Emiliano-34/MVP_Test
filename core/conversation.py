from collections import deque

class ConversationManager:
    def __init__(self, max_turns=10):
       
        # deque maxlen para olvidar lo viejo
        self.history = deque(maxlen=max_turns) 
        
    def add_message(self, role, content):
        # historial
        self.history.append({"role": role, "content": content})
        
    def get_history(self):
        # lista del historial que se envia a la API
        return list(self.history)

    def detect_intent(self, text):
        
        # Detecta si el usuario quiere una acción específica.
        
        text = text.lower().strip()
        if text.startswith("/nota"):
            return "guardar_nota"
        elif text.startswith("/recordatorio"):
            return "crear_recordatorio"
        elif text.startswith("/busqueda"):
            return "buscar"
        return "chat_general"
