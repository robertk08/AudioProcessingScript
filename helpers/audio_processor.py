import logging
from pydub import AudioSegment
from .utils import timestamp_to_ms

def match_target_amplitude(sound, audio_settings):
    target_dBFS = audio_settings.get("target_dBFS", -20.0)
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def trim_song(input_path, output_path, start_time, config, audio_settings):
    duration_sec = config.get("default_clip_duration_seconds", 30)
    normalize = audio_settings.get("normalize", True)
    fade_in_enabled = audio_settings.get("fade_in", False)
    fade_in_duration = audio_settings.get("fade_in_duration_ms", 0)
    fade_out_enabled = audio_settings.get("fade_out", False)
    fade_out_duration = audio_settings.get("fade_out_duration_ms", 0)
    audio_format = audio_settings.get("format", "mp3")
    bitrate = audio_settings.get("bitrate", None)
    sample_rate = audio_settings.get("sample_rate", None)

    start_ms = timestamp_to_ms(start_time)

    try:
        audio = AudioSegment.from_file(input_path)
        end_ms = start_ms + duration_sec * 1000
        snippet = audio[start_ms:min(end_ms, len(audio))].set_channels(2)

        if normalize:
            snippet = match_target_amplitude(snippet, audio_settings)
        if fade_in_enabled and fade_in_duration > 0:
            snippet = snippet.fade_in(fade_in_duration)
        if fade_out_enabled and fade_out_duration > 0:
            snippet = snippet.fade_out(fade_out_duration)

        export_kwargs = {}
        if bitrate and audio_format.lower() == "mp3":
            export_kwargs["bitrate"] = bitrate
        if sample_rate:
            export_kwargs["parameters"] = ["-ar", str(sample_rate)]

        snippet.export(output_path, format=audio_format, **export_kwargs)
        return True
    except Exception as e:
        logging.error(f"Error while trimming: {e}")
        return False
