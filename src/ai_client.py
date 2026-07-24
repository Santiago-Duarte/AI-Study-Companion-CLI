"""
Módulo ai_client para interactuar con la API de Google Gemini.

Este módulo proporciona funcionalidad para generar resúmenes de texto
y tarjetas de estudio utilizando el modelo de lenguaje Gemini de Google.
"""

import os
import time

from dotenv import load_dotenv
from google import genai


def generate_summary(text_chunk: str, api_key: str | None = None, max_retries: int = 3) -> str | None:
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

    for intento in range(max_retries):
        try:
            # 4. Hacer la petición al modelo (usamos gemini-2.5-flash por velocidad y costo)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            # 5. Devolver el texto de la respuesta
            return response.text if response.text else ""

        except Exception as e:
            catch_error_due_to_lack_of_tokens(e, intento, max_retries)

    return ""


def generate_flashcards(text_chunk: str, api_key: str | None = None, max_retries: int = 3) -> list[tuple[str, str]]:
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
        "Eres un asistente educativo de alto rendimiento especializado en síntesis extrema. "
        "Resume el siguiente fragmento de transcripción de YouTube.\n\n"
        "REGLAS OBLIGATORIAS:\n"
        "- Sé ultra conciso y ve directo al punto.\n"
        "- Extrae únicamente de 3 a 5 puntos clave (bullet points).\n"
        "- Cada punto debe ser una sola oración clara y directa.\n"
        "- No agregues introducciones, conclusiones ni texto de relleno.\n"
        "- Usa formato Markdown.\n\n"
        f"Transcripción:\n{text_chunk}"
    )

    for intento in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            raw_text = response.text if response.text else ""
            return parse_flashcards_response(raw_text)

        except Exception as e:
            catch_error_due_to_lack_of_tokens(e, intento, max_retries)

    return[]


def parse_flashcards_response(raw_text: str) -> list[tuple[str, str]]:
    """
    Convierte la respuesta en texto plano de Gemini en una lista de tuplas (pregunta, respuesta).

    Esta función procesa el texto plano generado por la API de Gemini y extrae
    las tarjetas de estudio separadas por el delimitador '|||'. Filtra líneas
    que no contienen el delimitador o que tienen campos vacíos.

    Args:
        raw_text (str): El texto plano de respuesta de la API de Gemini.

    Returns:
        list[tuple[str, str]]: Una lista de tuplas donde cada tupla contiene
                               una pregunta y su respuesta correspondiente.

    Example:
        >>> parse_flashcards_response("¿Qué es X?|||Respuesta X\\n¿Qué es Y?|||Respuesta Y")
        [("¿Qué es X?", "Respuesta X"), ("¿Qué es Y?", "Respuesta Y")]
    """
    cards = []
    for line in raw_text.strip().splitlines():
        if "|||" in line:
            parts = line.split("|||", 1)
            q = parts[0].strip()
            a = parts[1].strip()
            if q and a:
                cards.append((q, a))
    return cards


def catch_error_due_to_lack_of_tokens(e, intento, max_retries):
    """
    Maneja errores de cuota de la API de Gemini implementando reintentos con espera.

    Esta función detecta errores HTTP 429 (Too Many Requests) y espera 15 segundos
    antes de permitir otro intento. Si no es un error de cuota o se agotaron los
    reintentos, lanza una excepción RuntimeError.

    Args:
        e (Exception): La excepción capturada de la API.
        intento (int): El número de intento actual (comienza en 0).
        max_retries (int): El número máximo de reintentos permitidos.

    Raises:
        RuntimeError: Si el error no es 429 o se agotaron los reintentos.
    """
    if "429" in str(e) and intento < max_retries - 1:
        tiempo_espera = 15
        print(
            f"Límite de cuota alcanzado. Esperando {tiempo_espera}s (Intento {intento + 1}/{max_retries})..."
        )
        time.sleep(tiempo_espera)
    else:
        # Captura de errores de red o credenciales inválidas
        raise RuntimeError(f"Error al conectar con la API de Gemini: {e}")
