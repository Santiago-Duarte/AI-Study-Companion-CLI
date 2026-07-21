"""
Módulo ai_client para interactuar con la API de Google Gemini.

Este módulo proporciona funcionalidad para generar resúmenes de texto
utilizando el modelo de lenguaje Gemini de Google.
"""

import os
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
            model="gemini-2.5-flash",
            contents=prompt,
        )

        # 5. Devolver el texto de la respuesta
        return response.text if response.text else ""

    except Exception as e:
        # Captura de errores de red o credenciales inválidas
        raise RuntimeError(f"Error al conectar con la API de Gemini: {e}")