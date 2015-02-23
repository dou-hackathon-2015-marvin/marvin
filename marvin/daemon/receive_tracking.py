import hashlib
import logging
import os
import mimetypes
import subprocess


CHUNK_SIZE = 10 * 1024  # 10 kb
DOWNLOAD_DIR = os.path.expanduser('~/Downloads/Marvin')

jobs = {}


def initiate_transfer(job_id, filename, total):
    jobs[job_id] = {
        'job_id': job_id,
        'filename': filename,
        'received': 0,
        'total': total,
    }

    with open(get_filename(job_id), 'w'):
        pass


def get_filename(job_id, part=True):
    job = jobs[job_id]
    f = os.path.join(DOWNLOAD_DIR, job['filename'])
    if part:
        f += ".part"
    return f


def append_chunk(job_id, chunk):
    with open(get_filename(job_id), 'a+') as f:
        f.write(chunk)


def finish_sending(job_id, expected_md5):
    filename = get_filename(job_id, part=False)
    received_md5 = hashlib.md5()
    with open(get_filename(job_id, part=True), 'rb') as file_obj:
        while True:
            chunk = file_obj.read(CHUNK_SIZE)
            if not chunk:
                break
            received_md5.update(chunk)
    received_md5 = received_md5.hexdigest()
    if expected_md5 != received_md5:
        logging.error("WRONG MD5: expected {} but got {}".format(expected_md5, received_md5))

        os.rename(get_filename(job_id, part=True), filename + '.error')
    else:
        os.rename(get_filename(job_id, part=True), filename)
        mime = mimetypes.guess_type(filename)[0]
        if mime and mime.startswith('image/'):
            subprocess.Popen(['xdg-open', filename])
        else:
            subprocess.Popen(['xdg-open', DOWNLOAD_DIR])
