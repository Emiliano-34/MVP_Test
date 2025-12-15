# MVP

Este proyecto es un MVP de un asistente digital inteligente diseñado para apoyar en tareas diarias, búsqueda y educación. Implementa una arquitectura robusta con manejo de errores, memoria conversacional y control de parámetros de inferencia.

## Stack Técnico

* **Lenguaje:** Python 3.11
* **LLM Provider:** Groq (Model: `llama3-8b-8192`).
* **Interfaz:** Streamlit.
* **Resiliencia:** Librería `tenacity` para manejo de retries y backoff.

## Configuración e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL_DEL_REPO>
    cd ai-copilot-mvp
    ```

2.  **Entorno Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Variables de Entorno:**
    Renombrar `.env.example` a `.env` y agregar API Key de Groq.
    ```
    GROQ_API_KEY=gsk_...
    ```

4.  **Ejecutar:**
    ```bash
    streamlit run app/web.pys
    ```

## Lógica y Decisiones Técnicas

### 1. Integración LLM (Services)
* Se implementó un cliente en `services/llm.py` con **Exponential Backoff**.
* **Timeouts:** Configurados implícitamente por la librería, con 3 reintentos máximos ante errores 429 (Rate Limit) o 5xx.
* **Parámetros:**
    * `Temperature: 0.7`: Balance entre creatividad y precisión.
    * `Max Tokens: 500`: Para respuestas concisas.

### 2. Gestión de Conversación (Core)
* **Memoria:** Implementada con `collections.deque` con un límite estricto de **10 turnos** para evitar desbordamiento de contexto.
* **Prompting:** Se utiliza un `System Prompt` persistente que define la personalidad y reglas de seguridad.
* **Intents:** Detección básica de comandos como `/nota`, `/recordatorio` y `/busqueda` para demostrar enrutamiento de lógica.

## Métricas y Pruebas

El sistema incluye 6 pruebas unitarias (`pytest tests/`) que validan:
* Integridad de la memoria y truncado.
* Detección correcta de intents.
* Estructura de mensajes enviada a la API.

### Desempeño Observado (Local)
* **Latencia promedio:** ~800ms por respuesta.
* **Tasa de éxito:** 100% en pruebas manuales de 20 turnos.
