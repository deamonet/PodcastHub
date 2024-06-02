import os
from uuid import uuid4


def download(url):
    work_dir = f"/tmp/podcast/{str(uuid4())}"
    os.system(f"mkdir -p {work_dir}")
    os.system(f"cd {work_dir} | you-get {url}")
    return work_dir
