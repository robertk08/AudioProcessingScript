import logging
from pathlib import Path
from pydub import AudioSegment
from typing import Union, Optional, Dict, Any
from .utils import timestamp_to_ms


def match_target_amplitude(sound: AudioSegment, audio_settings: Dict[str, Any]) -> AudioSegment:
    target_dBFS: float = audio_settings.get("target_dBFS", -20.0)
    return sound.apply_gain(target_dBFS - sound.dBFS)


def trim_song(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    start_time: str,
    config: Dict[str, Any],
    audio_settings: Dict[str, Any]
) -> bool:
    duration: int = config.get("default_clip_duration_seconds", 30)
    normalize: bool = audio_settings.get("normalize", True)
    fade_in: bool = audio_settings.get("fade_in", False)
    fade_in_ms: int = audio_settings.get("fade_in_duration_ms", 0)
    fade_out: bool = audio_settings.get("fade_out", False)
    fade_out_ms: int = audio_settings.get("fade_out_duration_ms", 0)
    audio_format: str = audio_settings.get("format", "mp3").lower()
    bitrate: Optional[str] = audio_settings.get("bitrate")
    sample_rate: Optional[int] = audio_settings.get("sample_rate")

    try:
        input_path = Path(input_path)
        if not input_path.exists():
            logging.warning(f"Input file does not exist: {input_path}")
            return False

        audio = AudioSegment.from_file(input_path)
        audio = AudioSegment(audio)  
        if not isinstance(audio, AudioSegment):
            logging.error(f"Loaded audio is not an AudioSegment: {type(audio)}")
            return False
        start_ms: Optional[int] = timestamp_to_ms(start_time)
        if start_ms is None or start_ms >= len(audio):
            logging.error(f"Invalid timestamp or out of range: {start_time} ({start_ms}ms) in {input_path}")
            return False

        end_ms: int = min(start_ms + duration * 1000, len(audio))
        snippet = audio[start_ms:end_ms]
        snippet = snippet.set_channels(2)  # type: ignore[attr-defined]

        if normalize:
            snippet = match_target_amplitude(snippet, audio_settings)
        if fade_in and fade_in_ms > 0:
            snippet = snippet.fade_in(fade_in_ms)
        if fade_out and fade_out_ms > 0:
            snippet = snippet.fade_out(fade_out_ms)

        export_kwargs: Dict[str, Any] = {}
        if bitrate and audio_format == "mp3":
            export_kwargs["bitrate"] = bitrate
        if sample_rate:
            export_kwargs["parameters"] = ["-ar", str(sample_rate)]

        snippet.export(str(output_path), format=audio_format, **export_kwargs)
        logging.info(f"Exported trimmed audio to {output_path}")
        return True
    except Exception as e:
        logging.error(f"Error processing '{input_path}': {e}")
        return False