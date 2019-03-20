# http-logmon

A simple console program to parse live HTTP logs and output useful information
and alerts

## Usage

### Running

```
# from root dir
pip3 install -e .
```

# How I'd Improve the Program

Given more time, I might do some of the following:

- Move core alerting logic out of the main module into a separate module,
  similarly to what I've done with the storage modules.
  - Add alert/incident UUIDs.
- End-to-end functional tests, especially since there is already a script to
  generate recent test data.
- Consider multiplexing log parsing depending on the amount of traffic and
  system resources. However, I expected this to be run on a customer host where
  we wouldn't want significant resource consumption, so I kept it to 2
  additional threads (one for display/alert loop, one for consuming the log).
- Add additional storage implementations.
    - Similarly, set a limit on the amount of memory used by the in-memory
      simple storage implementation that I wrote.
- Add alerting extensions.
    - Notify Slack, IRC, email, etc.
- Possibly improve packaging if needed, in case we aren't running this in a
  Docker container or need to sidecar this inside an existing container.
- Possibly alter the alert text. I deviated from the one given by the
  assignment to also include useful information like the peak requests/second
  for the time the alert has been active, so you can see if the request load
  has been decreasing even when an alert's still active.
