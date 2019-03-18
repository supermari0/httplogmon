from concurrent.futures import ThreadPoolExecutor
from httplogmon import conf
from httplogmon.storage.simple import SimpleLogStorage


def poll_log_file():
    with open(conf.LOG_LOCATION, 'r') as f:
        while True:
            line = f.readline()
            if line:
                yield line


def monitor_logs(storage):
    for l in poll_log_file():
        storage.add_log_entry(storage)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        storage = SimpleLogStorage()
        poll_loop = executor.submit(monitor_logs, storage)
        # TODO: Poll every 10 seconds and alert if a problem exists, also add
        # alert to storage.
