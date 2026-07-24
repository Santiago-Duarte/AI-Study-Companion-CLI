"""
Módulo principal para ejecutar el pipeline de procesamiento de videos de YouTube.

Este módulo orquesta el flujo completo de trabajo: extracción de transcripciones,
procesamiento con IA para generar resúmenes y tarjetas de estudio, y guardado
de los resultados en archivos.
"""

import os
import tkinter as tk
from tkinter import filedialog

from formatter import save_markdown_summary, save_duocards_csv
from extractor import get_video_id, extract_transcript
from ai_client import generate_summary, generate_flashcards
from processor import chunk_text

from dotenv import load_dotenv
load_dotenv()


def procesar_resumen_completo(chunks: list[str]) -> str:
    """
    Procesa múltiples chunks de texto para generar un resumen completo.

    Esta función itera sobre una lista de fragmentos de texto, genera un
    resumen para cada uno usando la API de Gemini, y combina todos los
    resúmenes en un solo texto unido por doble salto de línea.

    Args:
        chunks (list[str]): Lista de fragmentos de texto a procesar.

    Returns:
        str: El resumen completo combinado de todos los chunks.
    """
    resumenes = []
    total = len(chunks)
    for i, chunk in enumerate(chunks, 1):
        if chunk:
            print(f"   ⏳ Procesando chunk {i}/{total} con Gemini...")
            summary = generate_summary(chunk)
            resumenes.append(summary)
    return "\n\n".join(resumenes)


def procesar_flashcards_completas(chunks: list[str]) -> list[tuple[str, str]]:
    """
    Procesa múltiples chunks de texto para generar tarjetas de estudio completas.

    Esta función itera sobre una lista de fragmentos de texto, genera
    tarjetas de estudio (flashcards) para cada uno usando la API de Gemini,
    y acumula todas las tarjetas en una sola lista.

    Args:
        chunks (list[str]): Lista de fragmentos de texto a procesar.

    Returns:
        list[tuple[str, str]]: Una lista acumulada de todas las tarjetas
                               generadas, donde cada tarjeta es una tupla
                               (pregunta, respuesta).
    """
    todas_las_tarjetas = []
    for chunk in chunks:
        if chunk:
            tarjetas = generate_flashcards(chunk)
            todas_las_tarjetas.extend(tarjetas)
    return todas_las_tarjetas


def run_pipeline(video_url: str, output_dir: str) -> None:
    """
    Orquesta el flujo completo de trabajo para procesar un video de YouTube.

    Esta función coordina todo el pipeline: extracción de la transcripción,
    fragmentación del texto, generación de tarjetas de estudio y guardado
    de los resultados en el directorio especificado.

    Args:
        video_url (str): La URL del video de YouTube a procesar.
        output_dir (str): El directorio donde se guardarán los archivos de salida.

    Returns:
        None

    Note:
        Actualmente solo genera tarjetas de estudio. La generación de resúmenes
        está comentada en el código.
    """
    if not output_dir:
        print("No se seleccionó ningún directorio de salida.")
        return

    print("Extrayendo la transcripción...")
    video_id = get_video_id(video_url)
    transcript = extract_transcript(video_id)

    print("Fragmentando el texto...")
    chunks = chunk_text(transcript)

    # Rutas absolutas a los archivos
    path_resumen = os.path.join(output_dir, "resumen.md")
    path_tarjetas = os.path.join(output_dir, "tarjetas.csv")

    print("Se esta generando el resumen: ")
    resumen_final = procesar_resumen_completo(chunks)
    save_markdown_summary(resumen_final, path_resumen)

    print("Se esta generando la flashcard: ")
    tarjetas_finales = procesar_flashcards_completas(chunks)
    save_duocards_csv(tarjetas_finales, path_tarjetas)

    print(f"Proceso completado: archivos guardados en: {output_dir}")


def main():
    """
    Función principal del programa.

    Solicita al usuario la URL de un video de YouTube, abre un diálogo
    para seleccionar el directorio de salida, y ejecuta el pipeline de
    procesamiento si se selecciona un directorio válido.
    """
    video_url = input("Ingrese la URL del video: ").strip()

    root = tk.Tk()
    root.withdraw()
    output_dir = filedialog.askdirectory(title="Selecciona el directorio de salida")
    root.destroy()  # Libera la ventana emergente correctamente

    if output_dir:
        run_pipeline(video_url, output_dir)
    else:
        print("Operación cancelada.")


if __name__ == "__main__":
    main()