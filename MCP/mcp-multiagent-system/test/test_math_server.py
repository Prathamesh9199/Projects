import subprocess
import json
import sys
import time
import re

def wait_for_json_response(proc):
    """
    Reads lines from the subprocess until it gets a valid JSON-RPC response.
    """
    buffer = ""
    while True:
        line = proc.stdout.readline()
        if not line:
            continue

        line = line.strip()

        # Skip banners, empty lines, and logs
        if not line or not line.startswith("{"):
            continue

        try:
            parsed = json.loads(line)
            return parsed
        except json.JSONDecodeError:
            buffer += line
            try:
                return json.loads(buffer)
            except json.JSONDecodeError:
                continue

def send_jsonrpc(proc, request):
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()
    return wait_for_json_response(proc)

# Start the server
proc = subprocess.Popen(
    [sys.executable, "servers/math_server/main.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1  # Line-buffered
)

try:
    print("Initializing...")
    init_req = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "1.0",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0"}
        }
    }
    init_resp = send_jsonrpc(proc, init_req)
    print(json.dumps(init_resp, indent=2))

    print("Calling add...")
    add_req = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {
            "name": "add",
            "arguments": {"a": 3, "b": 4}
        }
    }
    add_resp = send_jsonrpc(proc, add_req)
    print(json.dumps(add_resp, indent=2))

finally:
    proc.terminate()
