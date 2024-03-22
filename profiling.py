from subprocess import Popen, PIPE
import sys
import time
import json

if __name__ == "__main__":
    args = sys.argv[1:]
    with Popen(args, stdin=PIPE, stdout=PIPE, text=True) as test_harness_process:
        for line in sys.stdin:
            print(f"Received command {line.strip()}")
            print(f"Sending command to test harness...")
            test_harness_process.stdin.write(line)
            test_harness_process.stdin.flush()
            start_time = time.time()
            stdout = test_harness_process.stdout.readline().strip()
            end_time = time.time()
            elapsed_time_ms = (end_time - start_time) * (10**3)
            result_json = json.loads(stdout)
            # check if command wants perf data
            command = json.loads(line)
            if command["perf"] == True:
                result_json["perf"] = {
                    "elapsed_time_ms": elapsed_time_ms
                }
                print(f"Response from test harness (with added perf data): {json.dumps(result_json)}")
            else:
                print(f"Response from test harness: {json.dumps(result_json)}")