# 🎥 AI Video Study Companion

Una herramienta CLI modular construida en Python para extraer, procesar y transformar transcripciones de YouTube en artefactos de estudio estructurados (resúmenes en Markdown y tarjetas para DuoCards/Anki).

---

# 🛠️ Arquitectura del Proyecto

El proyecto sigue un diseño modular limpio con separación estricta entre la lógica de producción (`src/`) y la suite de pruebas unitarias (`tests/`).

```text
ai_video_study/
├── .env                  # Variables de entorno y API Keys
├── .gitignore            # Archivos excluidos del control de versiones
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Documentación principal
├── src/
│   ├── __init__.py
│   ├── main.py           # CLI / Punto de entrada de la aplicación
│   ├── extractor.py      # Extracción y limpieza de subtítulos de YouTube
│   ├── processor.py      # Segmentación (chunking) y procesamiento de texto
│   └── ai_client.py      # Cliente de conexión con la API de IA
└── tests/
    ├── __init__.py
    ├── test_extractor.py # Tests unitarios y mocks del extractor
    ├── test_processor.py # Tests del algoritmo de segmentación
    └── test_ai_client.py # Mocks de respuestas y excepciones de la IA
```

---

# 🚀 Módulos e Implementación

## 1. Extractor de Transcripciones (`src/extractor.py`)

### 🔹 Regex Quirúrgico
Normaliza y extrae IDs de 11 caracteres desde:

- URLs estándar (`watch?v=`)
- Enlaces acortados (`youtu.be/`)
- YouTube Shorts (`/shorts/`)

### 🔹 Resiliencia

Manejo explícito de excepciones nativas como:

- `TranscriptsDisabled`
- `NoTranscriptFound`

Esto evita caídas inesperadas durante la ejecución.

### 🔹 Rendimiento

Concatenación optimizada utilizando expresiones generadoras junto con `str.join()`, reduciendo el consumo de memoria.

---

## 2. Procesador y Segmentador de Texto (`src/processor.py`)

### 🔹 Algoritmo de Chunking Codicioso *(O(N))*

Divide textos extensos respetando los límites de palabras, evitando cortar oraciones o términos a la mitad.

### 🔹 Gestión de Ventana de Contexto

Permite parametrizar el tamaño máximo de cada bloque mediante `max_chars` (por defecto `1000`), evitando exceder el contexto soportado por modelos de lenguaje (LLMs).

### 🔹 Manejo de Casos Límite

Filtra espacios en blanco y cadenas vacías para impedir la generación de bloques nulos.

---

# 🧪 Pruebas Unitarias y Mocks

El proyecto aplica prácticas avanzadas de testing utilizando:

- `unittest`
- `unittest.mock`

Esto garantiza estabilidad y reproducibilidad sin depender de conexiones reales a Internet.

## Cobertura de Tests

### 📌 Extractor

- Validación de múltiples formatos de URL mediante `self.subTest`.
- Aislamiento completo de llamadas a la red utilizando `@patch`.
- Simulación de excepciones mediante `side_effect`.

### 📌 Procesador (Chunking)

- Verificación de integridad del texto (el texto reconstruido debe ser idéntico al original).
- Auditoría del límite estricto de caracteres por bloque.

### 📌 Cliente de IA

- Mock de respuestas exitosas.
- Simulación de errores de la API.
- Verificación del manejo correcto de excepciones.

---

# ▶️ Ejecutar la Suite de Pruebas

Desde la raíz del proyecto ejecuta:

```bash
python -m unittest discover tests -v
```