"""
Módulo de pruebas para el cliente de IA (Google Gemini).

Este módulo contiene pruebas unitarias para verificar el funcionamiento
correcto de la función generate_summary que interactúa con la API de Gemini.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.ai_client import generate_summary


class AiClientTestCase(unittest.TestCase):
    """
    Clase de pruebas para el cliente de IA.

    Prueba la función generate_summary que genera resúmenes utilizando
    la API de Google Gemini, verificando el manejo de API keys,
    respuestas exitosas y errores de conexión.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.

        Este método se ejecuta antes de cada prueba individual.
        Configura una API key de prueba para usar en los tests.
        """
        self.api_key = "fake_test_key_123"

    def test_api_key_not_found(self):
        with patch.dict("os.environ", {} ,clear=True):
            with self.assertRaises(ValueError):
                generate_summary("Fragmento de texto", None)

    @patch("src.ai_client.genai.Client")
    def test_generate_summary_success(self, mock_genai_client):
        """Simula una llamada exitosa a la API de Gemini"""
        # 1. Configurar la respuesta simulada (Mock)
        mock_response = MagicMock()
        mock_response.text = "## Resumen de prueba\n- Punto clave 1"

        # Instancia del cliente devuelta por genai.Client(...)
        mock_client_instance = mock_genai_client.return_value
        mock_client_instance.models.generate_content.return_value = mock_response

        # 2. Ejecutar la función con una API Key explícita de prueba
        resultado = generate_summary("Texto de prueba", api_key=self.api_key)

        # 3. Aserciones
        self.assertEqual(resultado, "## Resumen de prueba\n- Punto clave 1")
        mock_client_instance.models.generate_content.assert_called_once()

    @patch("src.ai_client.genai.Client")
    def test_generate_summary_api_error_raises_runtime_error(self, mock_genai_client):
        mock_client_instance = mock_genai_client.return_value
        mock_client_instance.models.generate_content.side_effect = Exception("Error de red 500")

        with self.assertRaises(RuntimeError):
            generate_summary("Texto de prueba", api_key=self.api_key)

    @patch("src.ai_client.genai.Client")
    def test_generate_summary_uses_env_variable(self, mock_genai_client):
        """Verifica que si api_key es None, la función lea fake_test_key_123 del entorno"""
        mock_response = MagicMock()
        mock_response.text = "Resumen ok"
        mock_client_instance = mock_genai_client.return_value
        mock_client_instance.models.generate_content.return_value = mock_response

        # Simulamos que existe la variable de entorno
        with patch.dict("os.environ", {"fake_test_key_123": "fake_env_key"}):
            # Pasamos api_key=None explícitamente
            resultado = generate_summary("Texto de prueba", api_key=None)

        # Verificamos que genai.Client se haya inicializado con la llave del entorno
        mock_genai_client.assert_called_once_with(api_key="fake_env_key")
        self.assertEqual(resultado, "Resumen ok")