import requests
import json
import uuid
from requests.exceptions import ChunkedEncodingError

MCP_ENDPOINT = "http://localhost:8000/mcp/"

# Use a single requests.Session object to persist headers and cookies
session = requests.Session()
session.headers.update({
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
})

def send_jsonrpc_request_with_session(payload):
    try:
        print(f"\nSending JSON-RPC request to {MCP_ENDPOINT} using a shared session.")
        response = session.post(MCP_ENDPOINT, data=json.dumps(payload))
        return {
            'status': True,
            'response': response,
            'error': None
        }
    except Exception as e:
        return {
            'status': False,
            'error': str(e)
        }

def run_weather_client():
    print("→ Initializing weather server...")

    init_request = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
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
    
    session_id = None
    try:
        with requests.post(MCP_ENDPOINT, data=json.dumps(init_request), headers=session.headers, stream=True) as response:
            print("→ Initializing connection established.")
            print("→ Response status:", response.status_code)
            
            session_id = response.headers.get('mcp-session-id')
            if session_id:
                print(f"✅ Extracted session ID from headers: {session_id}")
            else:
                print("❌ Failed to extract session ID from response headers.")
                return

            session.headers.update({'mcp-session-id': session_id})
            
            is_initialized = False
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data:'):
                    try:
                        json_data = json.loads(line[5:].strip())
                        print(f"Received JSON-RPC message: {json.dumps(json_data)}")
                        if 'result' in json_data and 'capabilities' in json_data['result']:
                            print("✅ Received initialization result. Server is ready.")
                            is_initialized = True
                            break
                    except json.JSONDecodeError:
                        pass
            
            if not is_initialized:
                print("❌ Initialization failed. Server did not send a completion message.")
                return

    except ChunkedEncodingError as e:
        print(f"An error occurred while reading the stream: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Now that initialization is complete, we can send subsequent requests.
    print("\n\n\n→ Calling temperature...")
    temp_request = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/call",
        "params": {
            "key": "temperature",
            "arguments": {
                "location": "London"
            }
        }
    }
    temp_response = send_jsonrpc_request_with_session(temp_request)
    if temp_response['status']:
        print("→ Response status:", temp_response['response'].status_code)
        print("→ Response headers:", temp_response['response'].headers)
        print("→ Raw body:", temp_response['response'].text)
    else:
        print("Error calling temperature tool:", temp_response['error'])

    print("\n\n\n→ Calling rain...")
    rain_request = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "tools/call",
        "params": {
            "key": "rain",
            "arguments": {
                "location": "Tokyo"
            }
        }
    }
    
    rain_response = send_jsonrpc_request_with_session(rain_request)
    if rain_response['status']:
        print("→ Response status:", rain_response['response'].status_code)
        print("→ Response headers:", rain_response['response'].headers)
        print("→ Raw body:", rain_response['response'].text)
    else:
        print("Error calling temperature tool:", rain_response['error'])

if __name__ == "__main__":
    run_weather_client()