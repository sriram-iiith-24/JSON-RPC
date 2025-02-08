import json
import sys

def generateServerCode(path):
    try:
        with open(path, 'r') as cp:
            contract = json.load(cp)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading contract file: {str(e)}")
        sys.exit(1)
    
    serverCode = """
import socket
import json
import inspect
import sys
from server_procedure import *

class RPCError(Exception):
    pass

def validate_function(func, params):
    sig = inspect.signature(func)
    param_count = len(sig.parameters)
    if param_count != len(params):
        raise RPCError(f"Parameter count mismatch. Expected {param_count}, got {len(params)}")
    return True

def handle_request(request):
    try:
        if not isinstance(request, dict):
            return {'error': 'Invalid request format'}
            
        procName = request.get('procedure')
        if not procName:
            return {'error': 'No procedure specified'}
            
        params = request.get('params', {})
        if not isinstance(params, dict):
            return {'error': 'Invalid parameters format'}
        
        try:
            func = globals()[procName]
        except KeyError:
            return {'error': f'Procedure {procName} not found'}
            
        if not callable(func):
            return {'error': f'{procName} is not a callable function'}
            
        try:
            validate_function(func, params)
            result = func(**params)
            return {'result': result}
        except TypeError as e:
            return {'error': f'Parameter mismatch: {str(e)}'}
        except Exception as e:
            return {'error': f'Function execution error: {str(e)}'}
            
    except Exception as e:
        return {'error': f'Server error: {str(e)}'}

def start_server(host='localhost', port=9999):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(10)
        print(f"Server running on {host}:{port}")
        
        while True:
            try:
                client, addr = server_socket.accept()
                try:
                    data = client.recv(4096).decode()
                    if not data:
                        continue
                    try:
                        request = json.loads(data)
                    except json.JSONDecodeError:
                        response = {'error': 'Invalid JSON request'}
                    else:
                        response = handle_request(request)
                    client.sendall(json.dumps(response).encode())
                except Exception as e:
                    client.sendall(json.dumps({'error': str(e)}).encode())
                finally:
                    client.close()
            except Exception as e:
                print(f"Connection error: {str(e)}")
                continue
    except Exception as e:
        print(f"Server error: {str(e)}")
        sys.exit(1)
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()
"""
    
    try:
        with open('rpc_server.py', 'w') as f:
            f.write(serverCode)
    except IOError as e:
        print(f"Error writing server code: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    generateServerCode(sys.argv[1])