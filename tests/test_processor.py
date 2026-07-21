"""
Módulo de pruebas para el procesador de texto.

Este módulo contiene pruebas unitarias para verificar el funcionamiento
correcto del algoritmo de chunking que divide textos largos en fragmentos
más pequeños respetando límites de caracteres.
"""

import unittest
from src.processor import chunk_text


class TestProcessor(unittest.TestCase):
    """
    Clase de pruebas para el módulo processor.

    Prueba la función chunk_text que divide textos en fragmentos
    respetando límites de caracteres sin cortar palabras.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.

        Este método se ejecuta antes de cada prueba individual.
        Configura textos de prueba con diferentes características:
        - Texto corto: Para probar casos simples
        - Texto vacío: Para probar casos límite
        - Texto largo: Para probar la división en múltiples chunks
        """
        self.texto_corto = "Hola mundo esto es un test"
        self.texto_vacio = "    "
        # Usamos .strip() para eliminar el espacio final descolgado
        self.texto_final = ("palabra " * 200).strip()

    def test_chunk_text(self):
        """
        Prueba la función chunk_text con diferentes casos de prueba.

        Verifica que:
        1. La cantidad de chunks generados sea la esperada
        2. El texto reconstruido sea idéntico al original (sin pérdida de palabras)

        Test cases:
        - Texto corto: Debe generar un solo chunk
        - Texto largo: Debe generar múltiples chunks
        - Texto vacío: Debe generar cero chunks
        """
        test_cases = [
            {"texto": self.texto_corto, "expected_len": 1},
            {"texto": self.texto_final, "expected_len": 2},
            {"texto": self.texto_vacio, "expected_len": 0}
        ]

        # Ejecuta cada caso de prueba individualmente
        for case in test_cases:
            with self.subTest(case=case):
                chunks = chunk_text(case["texto"])

                # 1. Validar la cantidad de chunks generados
                self.assertEqual(len(chunks), case["expected_len"])

                # 2. Validar que no se perdió ninguna palabra al reconstruir el texto
                if case["expected_len"] > 0:
                    texto_reconstruido = " ".join(chunks)
                    self.assertEqual(texto_reconstruido, case["texto"].strip())

    def test_chunk_max_chars_limit(self):
        """
        Prueba que ningún chunk exceda el límite de caracteres especificado.

        Verifica estrictamente que todos los fragmentos generados respeten
        el límite máximo de caracteres, garantizando que el algoritmo
        de chunking funciona correctamente para textos largos.

        Este test es crítico para asegurar que los chunks puedan ser
        procesados por APIs con límites de contexto (como modelos de IA).
        """
        max_chars = 500
        chunks = chunk_text(self.texto_final, max_chars=max_chars)

        # Verifica que cada chunk no exceda el límite de caracteres
        for chunk in chunks:
            self.assertLessEqual(len(chunk), max_chars)