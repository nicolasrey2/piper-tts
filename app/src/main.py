import hashlib
import os
import subprocess
import time
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configuración Piper
VOZ = "/voces/es_AR-daniela-high.onnx"
SALIDA_DIR = "/outputs"
LENGTH_SCALE = "1.45"  # velocidad de reproduccion de la voz

os.makedirs(SALIDA_DIR, exist_ok=True)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = FastAPI(title="TTS Piper Argentina con Cache")

# Modelo de entrada
class TextoRequest(BaseModel):
    texto: str

def texto_a_audio(texto: str) -> str:
    """Genera o devuelve el audio de un texto usando cache"""
    start_time = time.time()
    hash_texto = hashlib.md5(texto.encode("utf-8")).hexdigest()
    archivo_salida = os.path.join(SALIDA_DIR, f"{hash_texto}.wav")

    if os.path.exists(archivo_salida):
        elapsed = time.time() - start_time
        logging.info(f"[CACHE] Encontrado: {archivo_salida} (tiempo: {elapsed:.3f}s)")
        return archivo_salida

    logging.info(f"[GENERANDO] {archivo_salida}")
    try:
        subprocess.run(
            ["python3", "-m", "piper", "-m", VOZ, "--length-scale", LENGTH_SCALE, "-f", archivo_salida],
            input=texto.encode("utf-8"),
            check=True
        )

        # Convertir en el mismo archivo (pisando con formato compatible con Asterisk)
        subprocess.run(
            ["sox", archivo_salida, "-r", "8000", "-c", "1", "-b", "16", archivo_salida],
            check=True
        )
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generando audio: {e}")
        raise RuntimeError(f"Error generando audio: {e}")

    elapsed = time.time() - start_time
    logging.info(f"[GENERADO] {archivo_salida} (tiempo: {elapsed:.3f}s)")
    return archivo_salida

# Endpoint
@app.post("/tts")
def tts(request: TextoRequest):
    if not request.texto.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    archivo_audio = texto_a_audio(request.texto)
    # devolver solo el nombre del archivo (no el binario)
    return {"archivo": os.path.basename(archivo_audio)}
