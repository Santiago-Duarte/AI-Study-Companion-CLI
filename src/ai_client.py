"""
Módulo ai_client para interactuar con la API de Google Gemini.

Este módulo proporciona funcionalidad para generar resúmenes de texto
y tarjetas de estudio utilizando el modelo de lenguaje Gemini de Google.
"""

import os
from dotenv import load_dotenv
from google import genai


def generate_summary(text_chunk: str, api_key: str | None = None) -> str | None:
    """
    Genera un resumen de un fragmento de texto utilizando la API de Gemini.

    Esta función envía un fragmento de texto a la API de Google Gemini
    para obtener un resumen estructurado en formato Markdown. Utiliza
    el modelo gemini-2.5-flash por su velocidad y costo eficiente.

    Args:
        text_chunk (str): El fragmento de texto a resumir.
        api_key (str | None): La API key de Gemini. Si no se proporciona,
                              se busca la variable de entorno GEMINI_API_KEY.

    Returns:
        str | None: El resumen generado en formato Markdown, o string vacío
                    si no hay respuesta.

    Raises:
        ValueError: Si no se encuentra la API key ni por parámetro ni en entorno.
        RuntimeError: Si hay un error al conectar con la API de Gemini.

    Example:
        >>> generate_summary("Texto largo a resumir...", "your-api-key")
        "## Resumen\\n- Punto clave 1\\n- Punto clave 2"
    """
    # 1. Obtener la API Key (del parámetro o del entorno)
    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key:
        raise ValueError("No se encontró la API Key. Configura GEMINI_API_KEY en tu entorno.")

    # 2. Inicializar el cliente oficial con la llave
    client = genai.Client(api_key=key)

    # 3. Definir las instrucciones para el modelo (Prompt)
    prompt = (
        "Eres un asistente educativo de alto rendimiento. "
        "Resume el siguiente fragmento de transcripción de YouTube en puntos clave claros, "
        "estructurados en formato Markdown:\n\n"
        f"{text_chunk}"
    )

    try:
        # 4. Hacer la petición al modelo (usamos gemini-2.5-flash por velocidad y costo)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        # 5. Devolver el texto de la respuesta
        return response.text if response.text else ""

    except Exception as e:
        # Captura de errores de red o credenciales inválidas
        raise RuntimeError(f"Error al conectar con la API de Gemini: {e}")


def generate_flashcards(text_chunk: str, api_key: str | None = None) -> list[tuple[str, str]]:
    """
    Genera tarjetas de estudio a partir de un fragmento de texto usando Gemini.

    Esta función envía un fragmento de texto a la API de Google Gemini
    para generar preguntas y respuestas de estudio en formato flashcard.
    Utiliza el modelo gemini-3.6-flash y un formato específico con
    delimitador '|||' para separar preguntas de respuestas.

    Args:
        text_chunk (str): El fragmento de texto para generar tarjetas.
        api_key (str | None): La API key de Gemini. Si no se proporciona,
                              se busca la variable de entorno GEMINI_API_KEY.

    Returns:
        list[tuple[str, str]]: Una lista de tuplas donde cada tupla contiene
                               una pregunta y su respuesta correspondiente.

    Raises:
        ValueError: Si no se encuentra la API key ni por parámetro ni en entorno.
        RuntimeError: Si hay un error al conectar con la API de Gemini.

    Example:
        >>> generate_flashcards("Texto sobre variables...", "your-api-key")
        [("¿Qué es una variable?", "Es un espacio en memoria..."), ...]
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("No se encontró la API Key. Configura GEMINI_API_KEY en tu entorno.")

    client = genai.Client(api_key=key)

    prompt = (
        "Eres un asistente educativo especializado en crear tarjetas de memoria (flashcards) para Anki/DuoCards. "
        "A partir de la siguiente transcripción, genera preguntas y respuestas directas sobre los conceptos clave.\n\n"
        "REGLAS STRICTAS DE FORMATO:\n"
        "- Genera una tarjeta por línea.\n"
        "- Usa exactamente el delimitador '|||' para separar la pregunta de la respuesta.\n"
        "- Ejemplo: ¿Qué es una variable?|||Es un espacio en memoria para almacenar datos.\n"
        "- No incluyas viñetas, números, títulos ni formato Markdown adicional.\n\n"
        f"Transcripción:\n{text_chunk}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        raw_text = response.text if response.text else ""
        return parse_flashcards_response(raw_text)

    except Exception as e:
        raise RuntimeError(f"Error al conectar con la API de Gemini: {e}")


def parse_flashcards_response(raw_text: str) -> list[tuple[str, str]]:
    """Convierte la respuesta en texto plano de Gemini en una lista de tuplas (pregunta, respuesta)."""
    cards = []
    for line in raw_text.strip().splitlines():
        if "|||" in line:
            parts = line.split("|||", 1)
            q = parts[0].strip()
            a = parts[1].strip()
            if q and a:
                cards.append((q, a))
    return cards