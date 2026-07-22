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
    """
    Exporta tarjetas de estudio a formato CSV compatible con DuoCards/Anki.

    Esta función recibe una lista de tuplas (pregunta, respuesta) y la guarda
    en un archivo CSV con el formato específico requerido por DuoCards y Anki.
    Incluye una fila de encabezado con "question" y "answer".

    Args:
        cards (list[tuple[str, str]]): Lista de tuplas donde cada tupla contiene
                                       una pregunta y su respuesta correspondiente.
        output_path (str): La ruta del archivo CSV donde se guardarán las tarjetas.

    Returns:
        None

    Raises:
        ValueError: Si la lista de tarjetas está vacía.

    Example:
        >>> cards = [("¿Capital de Francia?", "París"), ("¿2+2?", "4")]
        >>> save_duocards_csv(cards, "output/tarjetas.csv")
        Las tarjetas se han guardado en output/tarjetas.csv
    """
    if not cards:
        raise ValueError("La lista de tarjetas no puede estar vacía.")

    ensure_directory_exists(output_path)

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["question", "answer"])
        writer.writerows(cards)

    print(f"Las tarjetas se han guardado en {output_path}")


def ensure_directory_exists(path: str):
    """
    Asegura que el directorio padre de una ruta exista, creándolo si es necesario.

    Esta función extrae el directorio padre de la ruta proporcionada y
    crea el directorio si no existe. Es útil para garantizar que se pueda
    escribir archivos en rutas que incluyen directorios que aún no existen.

    Args:
        path (str): La ruta del archivo para la cual se debe asegurar
                    que el directorio padre exista.

    Returns:
        None

    Example:
        >>> ensure_directory_exists("output/archivos/resumen.md")
        # Crea el directorio "output/archivos" si no existe
    """
    directorio_padre = os.path.dirname(path)

    if directorio_padre and not os.path.exists(directorio_padre):
        os.makedirs(directorio_padre)