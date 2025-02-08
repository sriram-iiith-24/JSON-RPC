import json
import sys

def generateClientCode(path):
    try:
        with open(path, 'r') as cp:
            contract = json.load(cp)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading contract file: {str(e)}")
        sys.exit(1)
    
    clientCode = """
import socket
import json

class RPCError(Exception):
    pass

class ConnectionError(RPCError):
    pass

class ParameterError(RPCError):
    pass

def validate_params(params, expected_params):
    if len(params) != len(expected_params):
        raise ParameterError(f"Expected {len(expected_params)} parameters, got {len(params)}")
    return True

def make_request(proc_name, params, expected_params, host='localhost', port=9999):
    try:
        validate_params(params, expected_params)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            request = {'procedure': proc_name, 'params': params}
            try:
                sock.sendall(json.dumps(request).encode('utf-8'))
                data = sock.recv(4096)
                if not data:
                    raise ConnectionError("No response from server")
                response = json.loads(data.decode('utf-8'))
                if 'error' in response:
                    raise RPCError(response['error'])
                return response['result']
            except json.JSONDecodeError:
                raise RPCError("Invalid response from server")
    except socket.error as e:
        raise ConnectionError(f"Connection failed: {str(e)}")
    except Exception as e:
        raise RPCError(f"RPC Error: {str(e)}")
"""
    
    for proc in contract.get('remote_procedures', []):
        procName = proc.get('procedure_name')
        if not procName:
            continue
            
        params = proc.get('parameters', [])
        returnType = proc.get('return_type')
        paramList = []
        paramValues = []
        paramDefs = []
        
        for param in params:
            paramName = param.get('parameter_name')
            if not paramName:
                continue
            paramType = param.get('data_type', 'any')
            paramList.append(paramName)
            paramValues.append(f"'{paramName}': {paramName}")
            paramDefs.append({'name': paramName, 'type': paramType})
        
        paramList.extend(['host="localhost"', 'port=9999'])
        paramStr = ', '.join(paramList)
        valueStr = ', '.join(paramValues) if paramValues else ''
        
        clientCode += f"""
def {procName}({paramStr}):
    expected_params = {paramDefs}
    return make_request(
        proc_name='{procName}',
        params={{{valueStr}}},
        expected_params=expected_params,
        host=host,
        port=port
    )
"""
    
    try:
        with open('rpc_client.py', 'w') as f:
            f.write(clientCode)
    except IOError as e:
        print(f"Error writing client code: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    generateClientCode(sys.argv[1])
