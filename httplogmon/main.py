from httplogmon import conf
from httplogmon.storage.simple import SimpleLogStorage
from httplogmon.text import parse_http_log_line
from httplogmon.alert import RequestCountAlert

from concurrent.futures import ThreadPoolExecutor
import datetime
import time


def poll_log_file():
    with open(conf.LOG_LOCATION, 'r') as f:
        while True:
            line = f.readline()
            if line:
                yield line


def monitor_logs(storage):
    for l in poll_log_file():
        log_entry = parse_http_log_line(l)
        storage.add_log_entry(log_entry)


def update_and_print_alerts(stats, storage):
    # TODO
    # - Write a test and Dockerize
    print("Priting alerts...")
    should_alert = (stats.rps_two_minutes >= conf.RPS_ALERT_THRESOLD)
    if storage.active_alert and should_alert:
        print("updating alert")
        storage.active_alert.update(stats.rps_two_minutes)
        print("Active alert: " + str(storage.active_alert))
    elif storage.active_alert:
        print('stopping alert')
        storage.stop_alert()
        print("Alert cleared!")
    elif should_alert:
        print('makin new alert')
        alert = RequestCountAlert(stats.rps_two_minutes)
        print('new alert made')
        storage.add_alert(alert)
        print('added to storage')
        print("New alert: " + str(storage.active_alert))
    print('')
    print('Historical alerts:')
    for alert in storage.old_alerts:
        print(str(alert))


def display_stats_and_check_alerts(current_time, storage):
    stats = storage.stats_and_purge()
    print("HTTP log monitor")
    print(f"Current time: {current_time}")
    print("Average requests per second (last 2 minutes): " +
          str(stats.rps_two_minutes))
    print('')
    print("Information about last 10 seconds of requests:")
    print("Average requests per second: " +
          str(stats.rps_ten_seconds))
    print("Request counts by section: ")
    for section, count in stats.counts_by_section.items():
        print(section + " - " + str(count))
    print("Response code counts: ")
    for code, count in stats.counts_by_response_code.items():
        print(str(code) + " - " + str(count))
    print("Total bytes sent: " + str(stats.bytes_sent))
    print('')
    update_and_print_alerts(stats, storage)
    print("-" * 79)


def display_loop(storage):
    # TODO Replace mocked out calls to utcnow to call now as below instead.
    previous_display = (datetime.datetime.now(datetime.timezone.utc)
                        - datetime.timedelta(seconds=10))
    while True:
        now = datetime.datetime.now(datetime.timezone.utc)
        if (now - previous_display) >= datetime.timedelta(seconds=10):
            display_stats_and_check_alerts(now, storage)
            previous_display = now
        else:
            time.sleep(5)


if __name__ == '__main__':
    # TODO Handle SIGTERM and exceptions within the threads
    with ThreadPoolExecutor(max_workers=2) as executor:
        storage = SimpleLogStorage()
        poll_loop = executor.submit(monitor_logs, storage)
        event_loop = executor.submit(display_loop, storage)
        poll_loop.result()
