import hashlib
import subprocess
import time
import logging
import os
import tempfile
import shutil


def text_to_speech(texto: str, voz, salida_dir, length_scale) -> str:
    """Genera o devuelve el audio de un texto usando cache"""
    logging.info(f"[TTS] Generando TTS para: {texto}")
    start_time = time.time()
    hash_texto = hashlib.md5(texto.encode("utf-8")).hexdigest()
    archivo_salida = os.path.join(salida_dir, f"{hash_texto}.wav")

    if os.path.exists(archivo_salida):
        elapsed = time.time() - start_time
        logging.info(f"[CACHE] Encontrado: {archivo_salida} (tiempo: {elapsed:.3f}s)")

        # ── ACTUALIZAR TIMESTAMP ──
        os.utime(archivo_salida, None)  # None usa la hora actual para atime y mtime
        logging.info(f"[CACHE] Timestamp actualizado con touch: {archivo_salida}")
        return archivo_salida

    logging.info(f"[GENERANDO] {archivo_salida}")
    try:
        # Generar audio con Piper
        subprocess.run(
            ["python3", "-m", "piper", "-m", voz, "--length-scale", length_scale, "-f", archivo_salida],
            input=texto.encode("utf-8"),
            check=True
        )

        # Convertir a 8kHz, mono, 16-bit PCM usando archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_name = tmp.name

        subprocess.run(
            ["sox", archivo_salida, "-r", "8000", "-c", "1", "-b", "16", tmp_name],
            check=True
        )

        # Reemplazar el archivo original
        shutil.move(tmp_name, archivo_salida)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error generando audio: {e}")
        raise RuntimeError(f"Error generando audio: {e}")

    elapsed = time.time() - start_time
    logging.info(f"[GENERADO] {archivo_salida} (tiempo: {elapsed:.3f}s)")
    return archivo_salida