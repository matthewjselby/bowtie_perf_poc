from subprocess import Popen, PIPE
import sys
import time
import json

if __name__ == "__main__":
    args = sys.argv[1:]
    with Popen(args, stdin=PIPE, stdout=PIPE, text=True) as test_harness_process:
        for line in sys.stdin:
            print(f"Sending line to test harness: {line.strip()}")
            test_harness_process.stdin.write(line)
            test_harness_process.stdin.flush()
            start_time = time.time()
            stdout = test_harness_process.stdout.readline().strip()
            end_time = time.time()
            elapsed_time_ms = (end_time - start_time) * (10**3)
            result_json = json.loads(stdout)
            result_json["perf"] = {
                "elapsed_time_ms": elapsed_time_ms
            }
            print(f"Response with added perf data: {json.dumps(result_json)}")