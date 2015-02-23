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

    with open(get_path(job_id, part=True), 'w'):
        pass


def get_path(job_id, part=False):
    job = jobs[job_id]
    f = os.path.join(DOWNLOAD_DIR, job['filename'])
    if part:
        return f + '.part'
    return f


def append_chunk(job_id, chunk):
    with open(get_path(job_id, part=True), 'a+') as f:
        f.write(chunk)


def is_known_mimetype(mimetype):
    known_mimetypes = {
        'application/pdf', 'text/plain', 'application/msword',
        'application/vnd.ms-excel'
    }

    if mimetype.startswith('image/') or mimetype in known_mimetypes:
        return True


def finish_sending(job_id, expected_md5):
    path = get_path(job_id)
    path_part = get_path(job_id, part=True)
    path_error = path + '.error'

    received_md5 = hashlib.md5()
    with open(path_part, 'rb') as file_obj:
        while True:
            chunk = file_obj.read(CHUNK_SIZE)
            if not chunk:
                break
            received_md5.update(chunk)
    received_md5 = received_md5.hexdigest()
    if expected_md5 != received_md5:
        logging.error("WRONG MD5: expected {} but got {}".format(expected_md5, received_md5))

        os.rename(path_part, path_error)
    else:
        os.rename(path_part, path)
        mimetype = mimetypes.guess_type(path)[0]
        if mimetype and is_known_mimetype(mimetype):
            subprocess.Popen(['xdg-open', path])
        else:
            subprocess.Popen(['xdg-open', os.path.dirname(path)])
