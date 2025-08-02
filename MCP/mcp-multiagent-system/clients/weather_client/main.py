import subprocess
import json
import time

def run_weather_client():
    # Start the weather_server process
    process = subprocess.Popen(
        ["python", "servers/weather_server/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    def send_request(request: dict):
        request_json = json.dumps(request)
        process.stdin.write(request_json + "\n")
        process.stdin.flush()
        time.sleep(0.1)  # Give time for response
        return process.stdout.readline().strip()

    print("Initializing weather_server...")
    init_request = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "1.0",
            "capabilities": {},
            "clientInfo": {
                "name": "weather_client",
                "version": "1.0"
            }
        }
    }
    print(send_request(init_request))

    print("Calling temperature...")
    temp_request = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {
            "name": "temperature",
            "arguments": {
                "location": "London"
            }
        }
    }
    print(send_request(temp_request))

    print("Calling rain...")
    rain_request = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "tools/call",
        "params": {
            "name": "rain",
            "arguments": {
                "location": "Tokyo"
            }
        }
    }
    print(send_request(rain_request))

    process.terminate()

if __name__ == "__main__":
    run_weather_client()
