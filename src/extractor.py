"""
Módulo extractor para obtener transcripciones de videos de YouTube.

Este módulo proporciona funciones para extraer transcripciones de videos
de YouTube utilizando la API de YouTube Transcript API.
"""

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re


def extract_transcript(id_video: str) -> str:
    """
    Extrae la transcripción de un video de YouTube dado su ID.

    Esta función intenta obtener la transcripción del video en español o inglés.
    Si no se puede obtener la transcripción, devuelve un mensaje de error.

    Args:
        id_video (str): El ID del video de YouTube (11 caracteres alfanuméricos).

    Returns:
        str: La transcripción completa del video como un string con los textos
             concatenados, o un mensaje de error si no se pudo obtener.

    Example:
        >>> extract_transcript("X7X5QgRGiDc")
        "Este es el texto de la transcripción del video..."
    """
    try:
        # Intenta obtener la transcripción en español o inglés
        transcription = YouTubeTranscriptApi().fetch(id_video, languages=["es", "en"])
        # Concatena todos los fragmentos de texto en un solo string
        return " ".join([snippet.text for snippet in transcription])
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        # Retorna mensaje de error si no se puede obtener la transcripción
        return f"No se pudo obtener la transcripción: {e}"


def get_video_id(url: str) -> str | None:
    """
    Extrae el ID del video de una URL de YouTube.

    Esta función soporta múltiples formatos de URLs de YouTube:
    - Formato estándar: https://www.youtube.com/watch?v=VIDEO_ID
    - Formato corto: https://youtu.be/VIDEO_ID
    - Formato shorts: https://www.youtube.com/shorts/VIDEO_ID

    Args:
        url (str): La URL del video de YouTube.

    Returns:
        str | None: El ID del video (11 caracteres) si se encuentra en la URL,
                    o None si la URL no tiene un formato válido.

    Example:
        >>> get_video_id("https://www.youtube.com/watch?v=X7X5QgRGiDc")
        "X7X5QgRGiDc"
        >>> get_video_id("https://youtu.be/5F1pcSljraU")
        "5F1pcSljraU"
    """
    # Patrón regex para extraer el ID del video de diferentes formatos de URL
    patron = r"(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})(?:\?|&|$)"
    match = re.search(patron, url)
    # Retorna el ID si hay coincidencia, None en caso contrario
    return match.group(1) if match else None

