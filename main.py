import os
import sys

import moviepy
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips

IMAGE_DURATION = 2.0
FPS = 30


def get_files(in_path, spliterator="VideoEditor\\"):
    names = list(os.walk(in_path))[0][2]

    paths = []
    new_path = in_path
    if not new_path.endswith("\\"):
        new_path = new_path + "\\"

    new_path = new_path.split(spliterator)[1].replace("\\", "/")

    for n in names:
        paths.append(new_path + n)

    return paths


video_paths = get_files(sys.path[0] + "\\input\\video")
audio_path = "input/audio/audio.mp3"
img_path = "input/img/img.png"

video_count = 1

for path in video_paths:
    video_clip = VideoFileClip(path)
    image_clip = ImageClip(img_path)
    audio_clip = CompositeAudioClip(
        [AudioFileClip(audio_path)]
    )

    image_clip = moviepy.video.fx.all.resize(image_clip, (video_clip.w, video_clip.h))
    image_clip = image_clip.set_duration(IMAGE_DURATION)

    no_audio = video_clip.without_audio()

    concat_clip = concatenate_videoclips([no_audio, image_clip])

    video_duration = concat_clip.duration
    audio_duration = audio_clip.duration

    part = (video_duration - audio_duration) / 2 + 1

    first = concat_clip.subclip(0, part)
    mid = concat_clip.subclip(part, part + audio_duration)
    last = concat_clip.subclip(part + audio_duration, video_duration)

    mid.audio = audio_clip

    res = concatenate_videoclips([first, mid, last])
    res.write_videofile("output/output_" + str(video_count) + ".mp4", fps=FPS)
    video_count += 1
