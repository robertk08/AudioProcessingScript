import logging
from pathlib import Path
from pydub import AudioSegment

from .utils import timestamp_to_ms


def match_target_amplitude(sound, audio_settings):
    target_dBFS = audio_settings.get("target_dBFS", -20.0)
    change_in_dBFS = target_dBFS - sound.dBFS
    logging.debug(f"Applying gain of {change_in_dBFS:.2f}dB to match target {target_dBFS}dBFS")
    return sound.apply_gain(change_in_dBFS)


def trim_song(input_path, output_path, start_time, config, audio_settings):
    duration_sec = config.get("default_clip_duration_seconds", 30)
    normalize = audio_settings.get("normalize", True)
    fade_in_enabled = audio_settings.get("fade_in", False)
    fade_in_duration = audio_settings.get("fade_in_duration_ms", 0)
    fade_out_enabled = audio_settings.get("fade_out", False)
    fade_out_duration = audio_settings.get("fade_out_duration_ms", 0)
    audio_format = audio_settings.get("format", "mp3").lower()
    bitrate = audio_settings.get("bitrate")
    sample_rate = audio_settings.get("sample_rate")

    try:
        input_path = Path(input_path)
        if not input_path.exists():
            logging.warning(f"trim_song: Input file does not exist: {input_path}")
            return False

        logging.debug(f"Loading audio from {input_path}")
        audio = AudioSegment.from_file(input_path)
        start_ms = timestamp_to_ms(start_time)

        if start_ms is None or start_ms >= len(audio):
            logging.error(f"trim_song: Invalid timestamp or out of range: {start_time} ({start_ms}ms) in {input_path}")
            return False

        end_ms = min(start_ms + duration_sec * 1000, len(audio))
        snippet = audio[start_ms:end_ms]
        if snippet.channels != 2:
            snippet = snippet.set_channels(2)

        if normalize:
            snippet = match_target_amplitude(snippet, audio_settings)

        if fade_in_enabled and fade_in_duration > 0:
            snippet = snippet.fade_in(fade_in_duration)

        if fade_out_enabled and fade_out_duration > 0:
            snippet = snippet.fade_out(fade_out_duration)

        export_kwargs = {}
        if bitrate and audio_format == "mp3":
            export_kwargs["bitrate"] = bitrate
        if sample_rate:
            export_kwargs["parameters"] = ["-ar", str(sample_rate)]

        logging.debug(f"Exporting audio to {output_path} as {audio_format}")
        snippet.export(output_path, format=audio_format, **export_kwargs)
        logging.info(f"trim_song: Exported trimmed audio to {output_path}")
        return True

    except Exception as e:
        logging.error(f"trim_song: Error processing '{input_path}': {e}")
        return False