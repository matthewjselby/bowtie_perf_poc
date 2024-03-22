# Proof of Concept for Bowtie Perf

This is a proof of concept for performace profiling for use in [bowtie](https://github.com/bowtie-json-schema/bowtie) as specified in this [issue](https://github.com/json-schema-org/community/issues/605) as part of my proposal for [GSoC](https://summerofcode.withgoogle.com).

Bowtie orchestrates a number of Docker containers for running each [implementation](https://docs.bowtie.report/en/stable/implementers/#term-implementation) of the JSON Schema specification, sending commands via stdin to a [test harness](https://docs.bowtie.report/en/stable/implementers/#term-test-harness) running in the container, which then appropriately calls the implementation and sends back results via stdout.

The concept outlined here is one of many possible implementations under exploration, but serves as a starting point for implementation agnostic performance profiling *in Docker*.

The basic concept is to wrap each test harness in a profiling script that runs it as a subprocess in the Docker container spun up for the implementation, as shown in the diagram below:

![](assets/bowtie_perf_diagram.svg)

The current proof of concept uses a Python script, but other implementations are possible, including a compiled executable that could serve as an entrypoint.

In the current code, `profiling.py` is a wrapper script serving as an `ENTRYPOINT` to the docker container that will run a test harness. Commands for running the test harness are specified in `CMD`. `CMD` arguments in a `Dockerfile` are passed to the `ENTRYPOINT` - so that in this circumstance `profiling.py` will receive the contents of `CMD`, which specifies how to run the test harness. In this case, the test harness is represented by `test.py`, so `CMD` is simply `python3 test.py`, which is passed to `profiling.py`.

The wrapper (`profiling.py`) starts the test harness (`test.py`) as a subprocess. Commands provided to the wrapper via stdin are then relayed to the test harness. Notably, commands can be relayed with some profiling code - in the example simple timing of how long the test harness takes to execute the command. More advanced profiling could include opening the subprocess for the test harness in some profiling wrapper such as `perf` or `bpftrace` and reading the results. Further, the wrapper illustrates parsing the input to determine if a `perf` attribute of the command is specified as true, and can do the profiling only when that condition is met.

The wrapper further parses the output from the test harness and adds a `perf` attribute, which includes information about performance of the implementation. In this proof of concept, that is simply how much time a given command took to execute in milliseconds, but this could be any data. Bowtie will need to be adapted to read in this additional information and take further action on it.

As an example, in the current proof of concept the container can be attached to and the following sent:

```text
{"cmd": "run", "seq": 1, "case": {}, "perf": true}
Received command {"cmd": "run", "seq": 1, "case": {}, "perf": true}
Sending command to test harness...
Response from test harness (with added perf data): {"cmd": "run", "res": "SUCCESS", "perf": {"elapsed_time_ms": 2502.040147781372}}
{"cmd": "run", "seq": 1, "case": {}, "perf": false}
Received command {"cmd": "run", "seq": 1, "case": {}, "perf": false}
Sending command to test harness...
Response from test harness: {"cmd": "run", "res": "SUCCESS"}
```

Note that the example test harness simply sleeps for 2.5 seconds before relaying `{"cmd": "[sent command]", "res": "SUCCESS"}` back via stdout. The wrapper times how long it takes for the test harness to respond and adds that data into the response.

Further exploration is needed to determine the best way to integrate this into current implementations. For example, can a Docker image with the wrapper as an entrypoint for use across implementations be published and used to prevent having to modify individual `Dockerfile`s? Perhaps a shell script or a compiled executable can be used instead of a Python script can be used here to reduce dependencies inside the Docker container.