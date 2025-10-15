import os
from pydub import AudioSegment
import pytest
import audio_concatenator

def create_dummy_wav(path):
    # Crear un WAV de 1 segundo silencio
    silent = AudioSegment.silent(duration=1000)
    silent.export(path, format="wav")

def test_concatenate(tmp_path):
    file1 = tmp_path / "a.wav"
    file2 = tmp_path / "b.wav"
    create_dummy_wav(file1)
    create_dummy_wav(file2)

    audios = [str(file1), str(file2)]

    output = audio_concatenator.concatenate(audios, str(tmp_path), mlsec_inter_concatenate=200)
    assert os.path.exists(output)

    # Comprobamos duración aproximada
    combinado = AudioSegment.from_wav(output)
    # duración >= suma de audios + silences
    assert combinado.duration_seconds >= 2 + (0.2*1)
