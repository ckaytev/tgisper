![Release](https://img.shields.io/github/v/release/ckaytev/tgisper.svg)
![Build](https://img.shields.io/github/actions/workflow/status/ckaytev/tgisper/ghcr-publish.yml.svg)
![Licence](https://img.shields.io/github/license/ckaytev/tgisper.svg)

# tgisper
Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multi-task model that can perform multilingual speech recognition as well as speech translation and language identification. For more details: [github.com/openai/whisper](https://github.com/openai/whisper/)

faster-whisper is a reimplementation of OpenAI's Whisper model using CTranslate2, which is a fast inference engine for Transformer models. For more details: [github.com/guillaumekln/faster-whisper](https://github.com/guillaumekln/faster-whisper/)

Tgisper is a bot for Telegram using a model from OpenAI to convert voice messages to text. It is enough to record a voice message or send it to the bot from another chat and you're done!


## Usage
```bash
docker run -d \
-e ASR_MODEL=small \
-e BOT_TOKEN=3916463517:ABC2tkTGkD9FHl4Ra-jv2Vv6DVECTyeV3Mm \
-e OMP_NUM_THREADS=2 \
ghcr.io/ckaytev/tgisper:main
```

## [Available models and languages](https://github.com/openai/whisper/#available-models-and-languages)



## Setup and run (Development Environment)

Install command-line tool [`ffmpeg`](https://ffmpeg.org/):

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

Install poetry with following command:

```sh
pip3 install poetry
```

Install packages:

```sh
poetry install
```

Set environment variable:
```sh
export BOT_TOKEN=3916463517:ABC2tkTGkD9FHl4Ra-jv2Vv6DVECTyeV3Mm

# The list of available models (https://github.com/openai/whisper/#available-models-and-languages)
export ASR_MODEL=base 

# When running on CPU, make sure to set the same number of threads
export OMP_NUM_THREADS=2
```

Starting the bot polling:

```sh
poetry run tgisper
```

With docker compose:

```sh
docker compose run -d -e BOT_TOKEN=3916463517:ABC2tkTGkD9FHl4Ra-jv2Vv6DVECTyeV3Mm tgisper
```