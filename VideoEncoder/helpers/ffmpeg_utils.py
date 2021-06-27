#  Copyright (C) 2021 The Authors

import os
import time
import ffmpeg
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import logging


def get_codec(filepath, channel="v:0"):
    output = check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            channel,
            "-show_entries",
            "stream=codec_name,codec_tag_string",
            "-of",
            "default=nokey=1:noprint_wrappers=1",
            filepath,
        ]
    )
    return output.decode("utf-8").split()


def encode(filepath):
    basefilepath = os.path.splitext(filepath)[0]
    output_filepath = basefilepath + ".HEVC" + ".mp4"
    assert output_filepath != filepath
    if os.path.isfile(output_filepath):
        logging.info('Skipping "{}": file already exists'.format(output_filepath))
        return None
    logging.info(filepath)
    # Get the video channel codec
    video_codec = get_codec(filepath, channel="v:0")
    if video_codec == []:
        logging.info("Skipping: no video codec reported")
        return None
    # Video transcode options
    if video_codec[0] == "hevc":
        if video_codec[1] == "hvc1":
            logging.info("Skipping: already h265 / hvc1")
            return None
        else:
            # Copy stream to hvc1
            video_opts = "-c:v copy -tag:v hvc1"
    else:
        # Transcode to h264
        video_opts = "-c:v libx264 -crf 29 -preset medium -tune animation -b:v 350k -threads 8"
    # Get the audio channel codec
    audio_codec = get_codec(filepath, channel="a:0")
    if audio_codec == []:
        audio_opts = ""
    elif audio_codec[0] == "libvorbis":
        audio_opts = "-c:a libopus"
    else:
        audio_opts = "-c:a libvorbis -b:a 60k -profile:a aac_he_v2 -ac 2 -vbr 2"
    call(
        ["ffmpeg", "-i", filepath]
        + video_opts.split()
        + audio_opts.split()
        + [output_filepath]
    )
    os.remove(filepath)
    return output_filepath


def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, "a").close()
    try:
        (
            ffmpeg.input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
        return None


def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
        return metadata.get("duration").seconds
    else:
        return 0


def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")
    else:
        return 856, 480
