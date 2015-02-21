from collections import namedtuple
import uuid

jobs = {}

(SENDING, FINISHED, QUEUED, PENDING, CANCELED, ERROR) = range(6)


JobStuct = namedtuple("job", ["id", "path", "total", "sent", "status"])


def send_file(filename, target_host, target_port):
    job_id = str(uuid.uuid4())
    jobs[job_id] = JobStuct(
        id=job_id,
        path=filename,
        total=1000,
        sent=0,
        status=QUEUED
    )
    return job_id


def is_in_progress(job):
    return job["status"] not in [CANCELED, ERROR, FINISHED]


def get_sending_jobs():
    return [job for job in jobs if is_in_progress(job["status"])]


def get_job(fid):
    return jobs[fid]
