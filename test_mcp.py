import subprocess
import json
import sys

def test_mcp_server():
    # Start the MCP server process
    proc = subprocess.Popen(
        [sys.executable, 'src/crawl4ai_mcp.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={'TRANSPORT': 'stdio'},
        text=True
    )
    
    try:
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test", "version": "1.0.0"}
            },
            "id": 1
        }
        
        print("Sending initialize request...")
        proc.stdin.write(json.dumps(init_request) + '\n')
        proc.stdin.flush()
        
        # Read response
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print("Initialize response:", json.dumps(response, indent=2))
        
        # Send tools/list request
        tools_request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 2
        }
        
        print("\nSending tools/list request...")
        proc.stdin.write(json.dumps(tools_request) + '\n')
        proc.stdin.flush()
        
        # Read response
        response_line = proc.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print("Tools response:", json.dumps(response, indent=2))
            
            if 'result' in response and 'tools' in response['result']:
                tools = response['result']['tools']
                print(f"\nFound {len(tools)} tools:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    test_mcp_server()
