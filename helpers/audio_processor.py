import logging
from typing import Dict, Any, Union
from pydub import AudioSegment
from .utils import timestamp_to_ms

def trim_song(input_path: str, output_path: str, start_time: str, config: Dict[str, Any], audio_settings: Dict[str, Any]) -> bool:
    duration_sec: int = config.get("default_clip_duration_seconds", 30)
    normalize: bool = audio_settings.get("normalize", True)
    fade_in_enabled: bool = audio_settings.get("fade_in", False)
    fade_in_duration: int = audio_settings.get("fade_in_duration_ms", 0)
    fade_out_enabled: bool = audio_settings.get("fade_out", False)
    fade_out_duration: int = audio_settings.get("fade_out_duration_ms", 0)
    audio_format: str = audio_settings.get("format", "mp3")
    bitrate: Union[str, None] = audio_settings.get("bitrate", None)
    sample_rate: Union[int, None] = audio_settings.get("sample_rate", None)

    try:
        audio: AudioSegment = AudioSegment.from_file(input_path)
        ts_result = timestamp_to_ms(start_time)
        if ts_result is None:
            return False
        if isinstance(ts_result, tuple):
            start_ms, end_ms = ts_result
            if not (0 <= start_ms < end_ms <= len(audio)):
                return False
        else:
            start_ms = ts_result
            end_ms = min(start_ms + duration_sec * 1000, len(audio))
        snippet: AudioSegment = audio[start_ms:end_ms].set_channels(2)  # type: ignore

        if normalize:
            target_dBFS: float = audio_settings.get("target_dBFS", -20.0)
            snippet = snippet.apply_gain(target_dBFS - snippet.dBFS)
        if fade_in_enabled and fade_in_duration > 0:
            snippet = snippet.fade_in(fade_in_duration)
        if fade_out_enabled and fade_out_duration > 0:
            snippet = snippet.fade_out(fade_out_duration)

        export_kwargs: Dict[str, Any] = {}
        if bitrate and audio_format.lower() == "mp3":
            export_kwargs["bitrate"] = bitrate
        if sample_rate:
            export_kwargs["parameters"] = ["-ar", str(sample_rate)]

        snippet.export(output_path, format=audio_format, **export_kwargs)
        return True
    except Exception as e:
        logging.error(f"Error while trimming: {e}")
        return False