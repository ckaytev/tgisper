# tgisper
Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multi-task model that can perform multilingual speech recognition as well as speech translation and language identification. For more details: [github.com/openai/whisper](https://github.com/openai/whisper/)

Tgisper is a bot for Telegram using a model from OpenAI to convert voice messages to text. It is enough to record a voice message or send it to the bot from another chat and you're done!

## Setup and run

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
export BOT_ID=3916463517:ABC2tkTGkD9FHl4Ra-jv2Vv6DVECTyeV3Mm

# The list of available models (https://github.com/openai/whisper/#available-models-and-languages)
export ASR_MODEL=base 
```

Starting the bot polling:

```sh
poetry run tgisper
```
