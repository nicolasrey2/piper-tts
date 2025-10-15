from pydub import AudioSegment
import os
import hashlib
import logging

def concatenate(audios: list[str], salida_dir: str, mlsec_inter_concatenate: int) -> str:
    """
    Concatena una lista de archivos wav en uno solo.
    mlsec_inter_concatenate: milisegundos de silencio entre audios.
    """
    hash_texto = hashlib.md5("".join(audios).encode("utf-8")).hexdigest()
    output_file = os.path.join(salida_dir, f"concatenated-{hash_texto}.wav")
    
    if os.path.exists(output_file):
        os.utime(output_file, None)  # None usa la hora actual para atime y mtime
        logging.info(f"[CACHE] Usando archivo concatenado existente: {output_file}")
        return output_file
    
    logging.info(f"[CONCATENANDO] {len(audios)} archivos...")
    silencio = AudioSegment.silent(duration=mlsec_inter_concatenate)  # 500 ms de silencio

    combinado = AudioSegment.empty()
    for i, archivo in enumerate(audios, 1):
        logging.info(f"  [{i}/{len(audios)}] Cargando {archivo}")
        sonido = AudioSegment.from_wav(archivo)
        combinado += sonido + silencio

    # Normalizar: 8 kHz, mono, 16-bit PCM
    combinado = combinado.set_frame_rate(8000) \
                         .set_channels(1) \
                         .set_sample_width(2)  # 16-bit = 2 bytes

    logging.info(f"[EXPORTANDO] {output_file}")
    combinado.export(output_file, format="wav")
    logging.info(f"[HECHO] Archivo concatenado generado: {output_file}")
    
    return output_file