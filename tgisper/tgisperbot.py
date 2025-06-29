import logging
import os
import signal
import subprocess
import sys
import time
from typing import BinaryIO

import ffmpeg
import numpy as np
import telebot
from faster_whisper import WhisperModel
from prometheus_client import start_http_server

from tgisper.metrics import DURATION_TIME
from tgisper.metrics import MESSAGES_TOTAL
from tgisper.metrics import PROCESSING_TIME

bot_token = os.getenv("BOT_TOKEN")
model_name = os.getenv("ASR_MODEL", "small")
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bot = telebot.TeleBot(bot_token)
model = WhisperModel(model_name, device="cpu", compute_type="float32")
SAMPLE_RATE = 16000


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hello! I'm a voice recognition bot 🎤 \
        \nRecord the voice or send it to me ↪️",
    )


@bot.message_handler(
    content_types=["voice"],
    chat_types=["private", "group", "supergroup"],
)
def transcribe_voice_message(message):
    start_time = time.perf_counter()
    labels = {
        "chat_type": message.chat.type,
        "content_type": message.content_type,
    }

    MESSAGES_TOTAL.labels(**labels).inc()

    try:
        logging.debug(
            f"Received voice message {message.message_id} "
            f"from chat {message.chat.id}"
        )
        voice_meta = bot.get_file(message.voice.file_id)
        voice_audio = load_audio(bot.download_file(voice_meta.file_path))
        segments, info = model.transcribe(
            audio=voice_audio,
            vad_filter=True,
            beam_size=1,
        )
        DURATION_TIME.labels(**labels).observe(info.duration)
        text = "".join(segment.text for segment in segments)
        bot.reply_to(message, text)
        logging.debug(
            f"Processed voice message {message.message_id} "
            f"from chat {message.chat.id}"
        )
    except Exception as e:
        logging.error(f"Error processing voice message: {e}")
    finally:
        PROCESSING_TIME.labels(**labels).observe(
            time.perf_counter() - start_time
        )


def load_audio(binary_file: BinaryIO, sr: int = SAMPLE_RATE):
    """Read an audio file object as mono waveform, resampling as necessary.

    Modified from https://github.com/openai/whisper/blob/main/whisper/audio.py
    to accept a binary object.

    Args:
        binary_file (BinaryIO): The audio file like object
        sr (int): The sample rate to resample the audio if necessary.

    Raises:
        RuntimeError: Failed to load audio
        RuntimeError: ffmpeg not found

    Returns:
        np.float32: A NumPy array containing the audio waveform
    """
    try:
        # Checking if ffmpeg is installed
        subprocess.run(
            ["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL
        )
    except FileNotFoundError:
        logging.error("ffmpeg not found")
        raise RuntimeError("ffmpeg not found")

    try:
        # This launches a subprocess to decode audio while down-mixing and
        # resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input("pipe:", threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(
                cmd="ffmpeg",
                capture_stdout=True,
                capture_stderr=True,
                input=binary_file,
            )
        )
    except ffmpeg.Error as e:
        logging.error(f"Failed to load audio: {e.stderr.decode()}")
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def handle_signal(sig, frame):
    logging.info("Stopping bot polling")
    bot.stop_polling()
    sys.exit(0)


def main():
    logging.info("Starting bot polling")
    start_http_server(8080)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    bot.infinity_polling(timeout=10, long_polling_timeout=5)


if __name__ == "__main__":
    main()
