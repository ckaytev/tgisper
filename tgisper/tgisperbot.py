import os
from typing import BinaryIO

import ffmpeg
import numpy as np
import telebot
from faster_whisper import WhisperModel

bot_id = os.getenv("BOT_ID")
model_name = os.getenv("ASR_MODEL", "small")

bot = telebot.TeleBot(bot_id)
model = WhisperModel(model_name, device="cpu", compute_type="float32")
SAMPLE_RATE = 16000


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        """
        Привет! Я бот для распознования голосовых сообщений 🎤
        Запиши голосовое или перешли его мне ↪️
        """,
    )


@bot.message_handler(content_types=["voice"])
def get_voice_message(message):
    voice_meta = bot.get_file(message.voice.file_id)
    voice_bytes = bot.download_file(voice_meta.file_path)
    voice_audio = load_audio(voice_bytes)
    segments, _ = model.transcribe(
        audio=voice_audio,
        vad_filter=True,
        beam_size=1,
    )
    text = ' '.join([segment.text for segment in segments])
    bot.send_message(message.from_user.id, text)


def load_audio(binary_file: BinaryIO, sr: int = SAMPLE_RATE):
    """Read an audio file object as mono waveform, resampling as necessary.

    Modified from https://github.com/openai/whisper/blob/main/whisper/audio.py
    to accept a binary object.

    Args:
        binary_file (BinaryIO): The audio file like object
        sr (int): The sample rate to resample the audio if necessary.

    Raises:
        RuntimeError: Failed to load audio

    Returns:
        np.float32: A NumPy array containing the audio waveform
    """
    try:
        # This launches a subprocess to decode audio while down-mixing and
        # resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input("pipe:", threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=binary_file)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def main():
    print("Start polling")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
