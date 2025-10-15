import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tts_service

# Configuración Piper
VOZ = "/voces/es_AR-daniela-high.onnx"
SALIDA_DIR = "/outputs"
LENGTH_SCALE = "1.45"           # velocidad de reproduccion de la voz
MILISECONDS_INTER_CONCAT = 500  # 500 milisegundos cuando se concatenan audios

os.makedirs(SALIDA_DIR, exist_ok=True)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = FastAPI(title="TTS Piper con Cache")

class TextoRequest(BaseModel):
    texto: str
    placeholders: list[str]

@app.post("/tts")
def tts(request: TextoRequest):
    if not request.texto.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    archivo_audio = tts_service.process(text=request.texto, placeholders=request.placeholders,
                            length_scale=LENGTH_SCALE, salida_dir=SALIDA_DIR, voz=VOZ,
                            mlsec_inter_concatenate=MILISECONDS_INTER_CONCAT)
    # devolver solo el nombre del archivo (no el binario)
    return {"archivo": os.path.basename(archivo_audio)}
