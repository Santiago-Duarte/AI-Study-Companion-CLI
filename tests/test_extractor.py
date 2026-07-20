"""
Módulo de pruebas para el extractor de transcripciones de YouTube.

Este módulo contiene pruebas unitarias para verificar el funcionamiento
correcto de las funciones de extracción de transcripciones y obtención
de IDs de videos de YouTube.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.extractor import extract_transcript, get_video_id
from youtube_transcript_api import TranscriptsDisabled


class TestYoutubeExtractor(unittest.TestCase):
    """
    Clase de pruebas para el módulo extractor.

    Prueba las funciones de extracción de transcripciones y obtención
    de IDs de videos de YouTube.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.

        Este método se ejecuta antes de cada prueba individual.
        Actualmente no requiere configuración específica.
        """
        pass

    def test_get_video_id_formats(self):
        """
        Prueba la extracción de IDs de videos desde diferentes formatos de URL.

        Verifica que la función get_video_id pueda extraer correctamente
        el ID del video desde URLs en diferentes formatos:
        - Formato estándar de YouTube
        - Formato corto (youtu.be)
        - Formato con parámetros adicionales

        Test cases:
        - URL estándar: https://www.youtube.com/watch?v=X7X5QgRGiDc
        - URL corta: https://youtu.be/5F1pcSljraU
        - URL con parámetros: https://www.youtube.com/watch?v=bjAdOUMFX5I
        """
        test_cases = [
            {"url":"https://www.youtube.com/watch?v=X7X5QgRGiDc", "expected_id":"X7X5QgRGiDc"},
            {"url":"https://youtu.be/5F1pcSljraU", "expected_id":"5F1pcSljraU"},
            {"url":"https://www.youtube.com/watch?v=bjAdOUMFX5I", "expected_id":"bjAdOUMFX5I"}
        ]

        # Ejecuta cada caso de prueba individualmente
        for case in test_cases:
            with self.subTest(case=case):
                self.assertEqual(get_video_id(case["url"]), case["expected_id"])

    @patch('src.extractor.YouTubeTranscriptApi')
    def test_extract_transcript_success(self, mock_api):
        """
        Prueba la extracción exitosa de una transcripción.

        Simula una respuesta exitosa de la API de YouTube Transcript
        y verifica que la función concatene correctamente los fragmentos
        de texto.

        Args:
            mock_api: Mock de la API de YouTube Transcript API.
        """
        # Configura el mock para retornar fragmentos de texto simulados
        mock_api.return_value.fetch.return_value = [
            unittest.mock.Mock(text="Hello"),
            unittest.mock.Mock(text="World")
        ]
        # Verifica que los fragmentos se concatenen correctamente
        self.assertEqual(extract_transcript("X7X5QgRGiDc"), "Hello World")

    @patch('src.extractor.YouTubeTranscriptApi')
    def test_extract_transcript_failure(self, mock_api):
        """
        Prueba el manejo de errores cuando no se puede obtener la transcripción.

        Simula un error de la API (subtítulos desactivados) y verifica
        que la función retorne un mensaje de error apropiado.

        Args:
            mock_api: Mock de la API de YouTube Transcript API.
        """
        # Configura el mock para lanzar una excepción de subtítulos desactivados
        mock_api.return_value.fetch.side_effect = TranscriptsDisabled("Subtítulos desactivados")
        # Verifica que se retorne un mensaje de error descriptivo
        resultado = extract_transcript("X7X5QgRGiDc")
        self.assertIn("No se pudo obtener la transcripción", resultado)
