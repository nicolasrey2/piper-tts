import os
import tempfile
import pytest
from unittest.mock import patch
import text_to_speech

def test_text_to_speech_cache(tmp_path):
    salida_dir = tmp_path
    texto = "hola mundo"
    voz = "voz_dummy"
    length_scale = "1.0"

    # Primera llamada: debería intentar generar audio
    with patch("subprocess.run") as mock_run:
        archivo = text_to_speech.text_to_speech(texto, voz, salida_dir, length_scale)
        mock_run.assert_called()  # se llamó a Piper

    # Crear archivo dummy para simular cache
    open(archivo, "w").close()

    # Segunda llamada: debería usar cache
    with patch("subprocess.run") as mock_run:
        archivo2 = text_to_speech.text_to_speech(texto, voz, salida_dir, length_scale)
        assert archivo == archivo2
        mock_run.assert_not_called()  # no debería llamar a Piper
