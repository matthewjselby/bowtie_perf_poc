from subprocess import Popen, PIPE
import sys
import json
from time import sleep

if __name__ == "__main__":
    for line in sys.stdin:
        sleep(2.5)
        command = json.loads(line)
        result = {
            "cmd": command["cmd"],
            "res": "SUCCESS"
        }
        sys.stdout.write(f"{json.dumps(result)}\n")
        sys.stdout.flush()