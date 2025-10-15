import re
from text_to_speech import text_to_speech
import audio_concatenator
import logging

def process(text: str, placeholders: list[str], voz, salida_dir, length_scale, mlsec_inter_concatenate) -> str:
    logging.info(f"[PROCESS] Texto recibido: {text}")
    logging.info(f"[PROCESS] Placeholders: {placeholders}")

    text_parts = [p.strip() for p in re.split(r"\{[^}]*\}", text) if p.strip()]

    if not placeholders:
        logging.info("[PROCESS] Sin placeholders, generando TTS directo")
        return text_to_speech(text_parts[0], voz, salida_dir, length_scale)

    if len(text_parts) != len(placeholders):
        raise ValueError("Cantidad de placeholders no coincide con texto")

    audios = [audio for par in zip(text_parts, placeholders) 
                for audio in (text_to_speech(par[0], voz, salida_dir, length_scale), 
                              text_to_speech(par[1], voz, salida_dir, length_scale))]

    logging.info(f"[PROCESS] Generados {len(audios)} audios, concatenando...")
    return audio_concatenator.concatenate(audios, salida_dir, mlsec_inter_concatenate)
