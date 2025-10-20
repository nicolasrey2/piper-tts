# TTS Piper con Cache

Este proyecto es un **servicio de Text-to-Speech (TTS)** basado en [Piper](https://github.com/rhasspy/piper) que convierte texto en audio.
Incluye **caché local**, de modo que si un texto ya fue convertido, devuelve el archivo existente en lugar de generar uno nuevo. Y tolera recibir textos con placeholders.

---

## Tecnologías usadas

* Python 3.11
* FastAPI
* Piper TTS
* Docker y Docker Compose
* ONNX para los modelos de voz

---

## Estructura del proyecto

```
.
├── app
│   ├── requirements.txt
│   ├── src
│   │   ├── audio_concatenator.py
│   │   ├── main.py
│   │   ├── text_to_speech.py
│   │   └── tts_service.py
│   └── tests
│       ├── test_audio_concatenator.py
│       ├── test_text_to_speech.py
│       └── test_tts_service.py
├── docker-compose.yml
├── Dockerfile
├── README.md
└── voces/  # NO se incluye en GitHub
```

> Nota: La carpeta `voces/` no se sube al repositorio porque los archivos son grandes (>100 MB).

---

## Uso con Docker Compose

1. **Construir y levantar el contenedor:**

```bash
docker compose up --build
```

2. El servicio TTS quedará expuesto en el puerto `8000` por defecto.

3. (Opcional) Para guardar los audios generados en tu máquina, podés habilitar un volumen en `docker-compose.yml`:

```yaml
volumes:
  - ./outputs:/outputs
```

---

## Descargar el modelo de voz

El proyecto usa el modelo **`es_AR-daniela-high.onnx`** de Piper. Para no subir archivos grandes al repo, se deben descargar manualmente:

```bash
mkdir -p voces
wget -O voces/es_AR-daniela-high.onnx https://huggingface.co/larcanio/piper-voices/resolve/main/es_AR-daniela-high.onnx
wget -O voces/es_AR-daniela-high.onnx.json https://huggingface.co/larcanio/piper-voices/resolve/main/es_AR-daniela-high.json
```

Asegurate de que los nombres de archivo coincidan con los definidos en `main.py`.

---

## Endpoint TTS

**URL:** `POST /tts`
**Contenido:** `application/json`

### Body's de ejemplo

```json
{
  "texto": "Hola, este es un ejemplo de TTS con Piper",
  "placeholders": ""
}
```
```json
{
  "texto": "Hola mi nombre es {nombre} y tengo {edad} años",
  "placeholders": ["nicolas", "20"]
}
```

### Respuesta

* Archivo WAV generado o concatenado o recuperado de la caché.
* Nombre del archivo: `audio.wav`
* `Content-Type: audio/wav`

### Ejemplo usando `curl`

```bash
curl -X POST "http://localhost:8000/tts" \
     -H "Content-Type: application/json" \
     -d '{ "texto": "Hola, este es un test", "placeholders": [] }'
```

Luego podés reproducirlo:

```bash
aplay audio.wav
# o en Windows/macOS usando tu reproductor favorito
```

---

## Configuración

* **Puerto:** `TTS_PORT` (por defecto `8000`)
* **Carpeta de salida de audios:** `/outputs`
* **Modelo de voz:** `/voces/es_AR-daniela-high.onnx`
* **Velocidad de la voz:** `LENGTH_SCALE` (por defecto `1.45`)

Estas variables están definidas en `main.py` y se pueden modificar según necesidad.

---

## Caché

* Cada texto enviado se convierte en un hash MD5.
* Si el texto ya fue procesado, se devuelve el archivo existente, evitando regenerarlo.

---

## Notas

* Asegurate de tener **Docker** y **Docker Compose** instalados.
* La primera generación de audio puede tardar más; las siguientes serán rápidas gracias a la caché.
* Compatible con Python ≥3.10.
* Los modelos de voz grandes se descargan con `wget` y **no se suben al repo** para evitar límites de GitHub.
