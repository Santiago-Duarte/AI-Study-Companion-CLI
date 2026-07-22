"""
Módulo de pruebas para el módulo formatter.

Este módulo contiene pruebas unitarias para verificar el funcionamiento
correcto de las funciones de guardado y formateo de contenido.
"""

import unittest
from unittest.mock import patch, mock_open
from src.formatter import ensure_directory_exists, save_markdown_summary, save_duocards_csv


class TestFormatter(unittest.TestCase):
    """
    Clase de pruebas para el módulo formatter.

    Prueba las funciones de guardado de resúmenes en Markdown y
    exportación de tarjetas de estudio en formato CSV.
    """

    def setUp(self):
        """
        Configuración inicial para cada prueba.

        Este método se ejecuta antes de cada prueba individual.
        Configura datos de prueba para usar en los tests.
        """
        self.contenido_prueba = "# Resumen\nEste es un texto."
        self.ruta_prueba = "output/resumen.md"
        self.csv_falso = [("Pregunta 1", "Respuesta 1"), ("Pregunta 2", "Respuesta 2")]

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_ensure_directory_exist_create_dir(self, mock_exists, mock_makedirs):
        """
        Prueba que ensure_directory_exists cree el directorio cuando no existe.

        Simula un escenario donde el directorio padre no existe y verifica
        que se llame a os.makedirs con el directorio correcto.

        Args:
            mock_exists: Mock de os.path.exists que retorna False.
            mock_makedirs: Mock de os.makedirs para verificar la llamada.
        """
        mock_exists.return_value = False
        ensure_directory_exists("test/archivo.md")
        mock_makedirs.assert_called_with("test")

    @patch("src.formatter.ensure_directory_exists")  # Para omitir la revisión del directorio
    @patch("builtins.open", new_callable=mock_open)
    def test_save_markdown_summary_writes_content(self, mock_file, mock_ensure_dir):
        """
        Prueba que save_markdown_summary escriba el contenido correctamente.

        Verifica que la función abra el archivo con los parámetros correctos
        y escriba el contenido proporcionado en el archivo.

        Args:
            mock_file: Mock de la función open para simular escritura de archivos.
            mock_ensure_dir: Mock de ensure_directory_exists para omitir creación de directorios.
        """
        # 1. Llamar a la función con los datos de prueba
        save_markdown_summary(self.contenido_prueba, self.ruta_prueba)

        # 2. Comprobar que open() se llamó con la ruta y los argumentos correctos
        mock_file.assert_called_once_with(self.ruta_prueba, "w", encoding="utf-8", newline="")

        # 3. Comprobar que write() se llamó con el contenido esperado
        mock_file().write.assert_called_once_with(self.contenido_prueba)


    def test_save_duocards_csv_empty_list_raises_error(self):
        """
        Prueba que save_duocards_csv lance ValueError cuando la lista de tarjetas está vacía.
        """
        with self.assertRaises(ValueError):
            save_duocards_csv([], "output/tarjetas.csv")

    @patch("src.formatter.ensure_directory_exists")
    @patch('builtins.open', new_callable=mock_open)
    def test_save_duocards_csv_writes_valid_data(self, mock_file, mock_ensure_dir):
        save_duocards_csv(self.csv_falso, self.ruta_prueba)
        mock_file.assert_called_once_with(self.ruta_prueba, "w", encoding="utf-8", newline="")
        mock_file().write.assert_called()
