import os
import youtube_dl
from .models import Task


def download(url: str, task_id: int, directory: str):
    """
    Use youtube-dl for downloads of mdia files
    for ytdl's options, see:
        https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
    """
    def hook(d):
        if d['status'] == 'finished':
            task = Task.query.get(task_id)
            if task:
                task.set_done(d['filename'])

    opts = {
        'format': 'bestaudio/best',
        'progress_hooks': [hook]
    }

    os.chdir(directory)

    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([url])
