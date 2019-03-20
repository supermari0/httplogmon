"""Application config."""

# Location to read HTTP logs from
DEFAULT_LOG_LOCATION = '/var/log/access.log'
# Thresold for requests per second above which to alert in a 2 minute sliding
# window
DEFAULT_RPS_ALERT_THRESHOLD = 10

RPS_ALERT_THRESOLD = DEFAULT_RPS_ALERT_THRESHOLD
LOG_LOCATION = DEFAULT_LOG_LOCATION
