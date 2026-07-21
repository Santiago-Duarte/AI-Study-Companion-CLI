"""
Módulo processor para procesar transcripciones de videos.

Este módulo coordina el flujo de trabajo para extraer transcripciones
de videos de YouTube y procesarlas con IA para generar resúmenes y
notas de estudio.
"""


def chunk_text(text: str, max_chars: int = 1000) -> list[str]:
    """
    Divide un texto largo en fragmentos más pequeños respetando límites de caracteres.

    Esta función implementa un algoritmo de chunking codicioso que divide el texto
    en bloques que no exceden el límite de caracteres especificado, evitando cortar
    palabras a la mitad. Es útil para procesar textos largos que deben enviarse a
    APIs con límites de contexto (como modelos de lenguaje).

    Args:
        text (str): El texto a dividir en fragmentos.
        max_chars (int): El número máximo de caracteres permitido por fragmento.
                         Por defecto es 1000.

    Returns:
        list[str]: Una lista de fragmentos de texto, donde cada fragmento
                   no excede max_chars caracteres.

    Example:
        >>> chunk_text("Hola mundo esto es un test", max_chars=10)
        ["Hola mundo", "esto es un", "test"]
        >>> chunk_text("palabra " * 200, max_chars=500)
        ["palabra palabra ...", "palabra palabra ..."]
    """
    chunks = []
    bloque_actual = []

    # Itera sobre cada palabra del texto
    for palabra in text.split():
        # Calcula el tamaño del bloque si se agrega la palabra actual
        tamanio_bloque = len(" ".join(bloque_actual + [palabra]))
        if tamanio_bloque <= max_chars:
            # Si el bloque no excede el límite, agrega la palabra
            bloque_actual.append(palabra)
        else:
            # Si excede el límite, guarda el bloque actual y empieza uno nuevo
            chunks.append(" ".join(bloque_actual))
            bloque_actual = [palabra]

    # Agrega el bloque restante si existe
    if bloque_actual:
        chunks.append(" ".join(bloque_actual))

    return chunks