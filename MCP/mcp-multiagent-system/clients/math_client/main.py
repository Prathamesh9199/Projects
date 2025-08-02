import subprocess
import json
import time

def run_math_client():
    # Start the math_server process
    process = subprocess.Popen(
        ["python", "servers/math_server/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    def send_request(request_json):
        process = subprocess.Popen(
            ["python", "servers/math_server/main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,          # ensures input/output are strings not bytes
            bufsize=1           # line-buffered
        )

        try:
            # Send the JSON-RPC request
            process.stdin.write(json.dumps(request_json) + "\n")
            process.stdin.flush()

            # Read the server's response
            response_line = process.stdout.readline()
            return json.loads(response_line)

        except Exception as e:
            return {"error": str(e)}

        finally:
            process.terminate()

    print("Initializing math_server...")
    init_request = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "1.0",
            "capabilities": {},
            "clientInfo": {
                "name": "math_client",
                "version": "1.0"
            }
        }
    }
    print(send_request(init_request))

    print("Calling add...")
    add_request = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {
            "name": "add",
            "arguments": {
                "a": 5,
                "b": 7
            }
        }
    }
    print(send_request(add_request))

    print("Calling subtract...")
    sub_request = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "tools/call",
        "params": {
            "name": "subtract",
            "arguments": {
                "a": 10,
                "b": 3
            }
        }
    }
    print(send_request(sub_request))

    print("Calling area_of_circle...")
    area_request = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "tools/call",
        "params": {
            "name": "area_of_circle",
            "arguments": {
                "radius": 4
            }
        }
    }
    print(send_request(area_request))

    process.terminate()

if __name__ == "__main__":
    run_math_client()
