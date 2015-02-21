import os

jobs = {}


def initiate_transfer(job_id, filename, total):
    jobs[job_id] = {
        "job_id": job_id,
        "filename": filename,
        "received": 0,
        "total": total,
    }

    with open(get_filename(job_id), "w"):
        pass


def get_filename(job_id):
    job = jobs[job_id]
    home = os.path.expanduser("~")
    return os.path.join(home, "Downloads", job["filename"])


def append_chunk(job_id, chunk):
    with open(get_filename(job_id), "a+") as f:
        f.write(chunk)
