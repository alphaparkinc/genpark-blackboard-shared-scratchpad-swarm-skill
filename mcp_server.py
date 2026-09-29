import sys
import json
from client import BlackboardSwarm

bb = BlackboardSwarm()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-blackboard-shared-scratchpad-swarm-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "post_blackboard_task",
                        "description": "Post new task to shared blackboard",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string"},
                                "description": {"type": "string"},
                                "capability": {"type": "string"}
                            },
                            "required": ["task_id", "description", "capability"]
                        }
                    },
                    {
                        "name": "contribute_blackboard_solution",
                        "description": "Contribute task resolution from agent to shared state",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "agent_id": {"type": "string"},
                                "task_id": {"type": "string"},
                                "result": {"type": "object"}
                            },
                            "required": ["agent_id", "task_id", "result"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "post_blackboard_task":
            bb.post_task(args.get("task_id"), args.get("description"), args.get("capability"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Task posted"}]}}
        elif tool_name == "contribute_blackboard_solution":
            ok = bb.contribute(args.get("agent_id"), args.get("task_id"), args.get("result"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"success": ok, "state": bb.state})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
