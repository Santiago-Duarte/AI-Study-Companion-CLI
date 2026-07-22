"""
Módulo formatter para guardar y formatear contenido de salida.

Este módulo proporciona funciones para guardar resúmenes en formato Markdown
y tarjetas de estudio en formato CSV compatible con DuoCards/Anki.
"""

import csv
import os


def save_markdown_summary(content: str, output_path: str) -> None:
    """
    Guarda un resumen en formato Markdown en la ruta especificada.

    Esta función guarda contenido de texto plano o Markdown en un archivo,
    creando el directorio padre si no existe. Utiliza codificación UTF-8
    para soportar caracteres especiales.

    Args:
        content (str): El contenido a guardar en formato Markdown.
        output_path (str): La ruta del archivo donde se guardará el contenido.

    Returns:
        None

    Example:
        >>> save_markdown_summary("# Resumen\\nContenido", "output/resumen.md")
        Resumen guardado en output/resumen.md
    """
    ensure_directory_exists(output_path)
    with open(output_path, "w", encoding="utf-8", newline="") as file:
        file.write(content)

    print(f"Resumen guardado en {output_path}")


def save_duocards_csv(cards: list[tuple[str, str]], output_path: str) -> None:
    """Recibe una lista de tuplas (pregunta, respuesta) y la exporta a CSV en formato compatible."""

    if not cards:
        raise ValueError("La lista de tarjetas no puede estar vacía.")

    ensure_directory_exists(output_path)

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["question", "answer"])
        writer.writerows(cards)

    print(f"Las tarjetas se han guardado en {output_path}")


def ensure_directory_exists(path: str):
    """Extrae el directorio padre de un path dado."""
    directorio_padre = os.path.dirname(path)

    if directorio_padre and not os.path.exists(directorio_padre):
        os.makedirs(directorio_padre)