import os

from configuration import CONFIG
from constant import FILE_EXTENSION_DELIMITER, AUDIO_EXTENSION
from entity.queue_task import QueueTask


def download_video(task: QueueTask):
    work_dir = f"{CONFIG.storage.video}/{task.name}/{task.identifier}"
    os.system(f"mkdir -p {work_dir}")
    for root, dirs, files in os.walk(work_dir):
        if len(files) != 0:
            return

    os.system(f"cd {work_dir} | you-get {task.prefix}/{task.identifier}")


def convert_video_to_audio(task: QueueTask):
    video_directory = f"{CONFIG.storage.video}/{task.name}/{task.identifier}"
    audio_directory = f"{CONFIG.storage.audio}/{task.name}/{task.identifier}"
    video_file = ""
    file_name = ""
    for root, dirs, files in os.walk(video_directory):
        for file in files:
            file_name, _ = file.split(FILE_EXTENSION_DELIMITER)
            video_file = root + file
            break
        break

    audio_file = f"{audio_directory}/{file_name}{AUDIO_EXTENSION}"
    if os.path.isfile(audio_file):
        return audio_file

    os.system(f"ffmpeg -i {video_file} -vn -acodec copy {audio_file}")
    return file_name
