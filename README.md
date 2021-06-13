# Video Encoder Bot
A Telegram bot to convert videos into x265/x264 format via ffmpeg.

### Configuration
Add values in environment variables or add them in [.env.sample](./.env.sample) and rename file to `.env`.
- `BOT_TOKEN` - Get it by creating a bot on [@BotFather](https://t.me/BotFather).
- `MONGO_URL` - Mongo Database URL.

### Configuring Encoding Format
To change the ffmpeg profile edit them in [ffmpeg_utils.py](/VideoEncoder/helpers/ffmpeg_utils.py)

### Installing Requirements
Install the required Python Modules in your machine.
```sh
apt-get -qq install ffmpeg
pip3 install -r requirements.txt
```
### Deployment
With python3.7 or later.
```sh
python3 -m VideoEncoder
```

### Credits
> *Thanks to [ShannonScott](https://gist.github.com/ShannonScott) for [transcode_h265.py](https://gist.github.com/ShannonScott/6d807fc59bfa0356eee64fad66f9d9a8).*    
> *Original work by [viperadnan](https://github.com/viperadnan-git/video-encoder-bot).*

### Copyright & License
- Copyright &copy; 2021 &mdash; [Adnan Ahmad](https://github.com/viperadnan-git); [xditya](https://xditya.me/github).
- Licensed under the terms of the [GNU General Public License Version 3 &dash; 29 June 2007](./LICENSE)
