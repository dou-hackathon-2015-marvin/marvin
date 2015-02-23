import os
import hashlib

from collections import namedtuple
import logging
from threading import Thread
import uuid
import time
from .internode_client import InternodeClient

jobs = {}

(SENDING, FINISHED, QUEUED, PENDING, CANCELED, ERROR) = range(6)


JobStuct = namedtuple("job", ["id", "path", "total", "sent", "status", "start_time", "target"])
JobStuct_signature = '(ssssiis)'

CHUNK_SIZE = 10 * 1024  # 10 kb


def save_job(job_id, data):
    jobs[job_id] = data


def load_job(job_id):
    return jobs[job_id]


class JobProcess(Thread):
    def __init__(self, job_id, host, port):
        super(JobProcess, self).__init__()
        self.job_id = job_id
        self.host = host
        self.port = port
        self.file_obj = None
        self.i_client = None

    def set_status(self, status):
        job_obj = load_job(self.job_id)
        job_obj = job_obj._replace(status=status)
        save_job(self.job_id, job_obj)

    def send_chunk(self):
        job_obj = load_job(self.job_id)
        chunk = self.file_obj.read(CHUNK_SIZE)
        self.i_client.send_chunk(self.job_id, chunk)
        job_obj = job_obj._replace(sent=str(long(job_obj.sent) + len(chunk)))
        save_job(self.job_id, job_obj)

        self.md5.update(chunk)

    def run(self):
        self.i_client = InternodeClient(self.host, self.port)

        self.set_status(PENDING)
        job_obj = load_job(self.job_id)
        is_approved = self.i_client.send_file_request(os.path.basename(job_obj.path), self.job_id, job_obj.total)
        logging.info("FILE REQUEST SENT: {}".format(is_approved))
        if is_approved:
            self.set_status(SENDING)
            self.md5 = hashlib.md5()
            with open(job_obj.path) as file_obj:
                self.file_obj = file_obj
                while long(job_obj.sent) < long(job_obj.total):
                    self.send_chunk()
                    job_obj = load_job(self.job_id)
            self.i_client.finish_sending(self.job_id, self.md5.hexdigest())
            self.set_status(FINISHED)
        else:
            self.set_status(CANCELED)


def send_file(filename, target_host, target_port):
    job_id = str(uuid.uuid4())
    save_job(job_id, JobStuct(
        id=job_id,
        path=filename,
        total=str(os.path.getsize(filename)),
        sent="0",
        status=QUEUED,
        start_time=int(time.time()),
        target=target_host
    ))
    thread = JobProcess(job_id, target_host, target_port)
    thread.start()
    return job_id


def is_in_progress(status):
    return status not in [CANCELED, ERROR, FINISHED]


def get_sending_jobs():
    return [job for job in jobs.values() if is_in_progress(job.status)]


def get_job(job_id):
    return load_job(job_id)


def create_test_job():
    return JobStuct(
        id="0e0fef87-612c-4b27-a43f-c9544ca69f57",
        path="/home/arturdent/testfile",
        total="1002",
        sent="0",
        status=SENDING,
        start_time=int(time.time()),
        target="127.0.0.1"
    )


def get_jobs():
    return [j for j in jobs.values()]
