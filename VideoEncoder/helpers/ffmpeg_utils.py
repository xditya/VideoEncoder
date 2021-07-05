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
    output_filepath = basefilepath + ".HEVC" + ".mp4" #Change .HEVC to what name you want before extension
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
        # video option read ffmpeg Documentation
        codec_opts = "-c:v libx265" #for h264 change libx265 to libx264
        profile_opts = "-profile:v high" #choose video profile you want
        tag_opts =  "-tag:v hvc1" #change to avc1 if want h264
        tune_opts = "-tune animation" #choose suitable tune 
        lvl_opts = "-level 3.1" #encoding level
        crf_opts = "-crf 24" #Constant rate factor lower is better quality but big size
        preset_opts = "-preset fast" #Choose preset more fast more worst quality
        core_opts = "-threads 8" #depends on yours cpu core
        audio_opts = "-c:a aac -b:a 128k" #choose audio format and bitrate you want
    call(
        ["ffmpeg", "-i", filepath]
        + codec_opts.split()
        + profile_opts.split()
        + crf_opts.split()
        + tag_opts.split()
        + preset_opts.split()
        + lvl_opts.split()
        + tune_opts.split()
        + core_opts.split()
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
        return 1280, 720
