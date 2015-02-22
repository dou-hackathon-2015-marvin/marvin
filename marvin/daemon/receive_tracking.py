import hashlib
import logging
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


def get_filename(job_id, part=True):
    job = jobs[job_id]
    home = os.path.expanduser("~")
    f = os.path.join(home, "Downloads", "Marvin", job["filename"])
    if part:
        f += ".part"
    return f


def append_chunk(job_id, chunk):
    with open(get_filename(job_id), "a+") as f:
        f.write(chunk)


def finish_sending(job_id, expected_md5):
    received_md5 = hashlib.md5(open(get_filename(job_id, part=True), 'rb').read()).hexdigest()
    if expected_md5 != received_md5:
        logging.error("WRONG MD5: expected {} but got {}".format(expected_md5, received_md5))

        os.rename(get_filename(job_id, part=True), get_filename(job_id, part=False) + ".error")
    else:
        os.rename(get_filename(job_id, part=True), get_filename(job_id, part=False))
