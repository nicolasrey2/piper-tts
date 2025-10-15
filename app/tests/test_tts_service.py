import pytest
from unittest.mock import patch
import tts_service

def test_process_no_placeholders(tmp_path):
    texto = "hola mundo"
    placeholders = []
    voz = "voz_dummy"
    length_scale = "1.0"
    mlsec_inter_concatenate = 500

    # IMPORTANTE: patchear donde se importa, no donde se define
    with patch("tts_service.text_to_speech") as mock_tts:
        mock_tts.return_value = str(tmp_path / "dummy.wav")
        output = tts_service.process(
            texto,
            placeholders,
            voz,
            str(tmp_path),
            length_scale,
            mlsec_inter_concatenate
        )

    assert output.endswith("dummy.wav")

def test_process_with_placeholders(tmp_path):
    text = "hola {nombre}"
    placeholders = ["nico"]
    voz = "voz_dummy"
    length_scale = "1.0"
    mlsec_inter_concatenate = 500

    with patch("tts_service.text_to_speech") as mock_tts, \
         patch("tts_service.audio_concatenator.concatenate") as mock_concat:

        mock_tts.side_effect = [
            str(tmp_path / "a.wav"),
            str(tmp_path / "b.wav")
        ]
        mock_concat.return_value = str(tmp_path / "final.wav")

        output = tts_service.process(
            text,
            placeholders,
            voz,
            str(tmp_path),
            length_scale,
            mlsec_inter_concatenate
        )

    assert output.endswith("final.wav")
