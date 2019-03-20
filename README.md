# http-logmon

A simple console program to parse live HTTP logs and output useful information
and alerts

## Usage

### Running

With Docker:

```
$ cd httplogmon
$ sudo docker build .
// run interactively so you can see output
$ sudo docker run -ti <docker_image_hash>
```

The above will generate log data to show the alerting behavior. To start with
an empty log, replace the docker run command above with:

```
sudo docker run -e GENDATA=false <docker_image_hash>
```

To run unit tests, replace the entrypoint with `/usr/src/run-tests.sh`.

```
$ sudo docker run --entrypoint "/usr/src/run-tests.sh" -it 16e8dd
```

You can edit the config in `httplogmon/main.py`, but this will require a new
Docker build.

# How I'd Improve the Program

Given more time, I might do some of the following:

- Allow configuration as environment variables. Currently, config is just
  stored in a Python module, so reconfiguration requires an image rebuild.
- Enforce PEP8 style.
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
