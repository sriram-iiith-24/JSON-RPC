# JSON-RPC

## Description
A custom Remote Procedure Call (RPC) system implementation that allows dynamic function calls between client and server using socket communication. The system generates client and server stubs based on a contract file, enabling remote function execution without using external RPC frameworks.

## Prerequisites
1. Python 3.x
2. No external packages required:
   - `socket`
   - `json`
   - `sys`

## Setup Instructions

1. **Project Structure Setup:**
   Create the following directory structure:
   ```
   project_root/
   ├── code_generator_client.py
   ├── code_generator_server.py
   ├── contract.json
   ├── server_procedure.py
   ├── client.py
   └── rpc_server.py (generated)
   └── rpc_client.py (generated)
   ```

2. **Generate RPC Code:**
   ```bash
   python code_generator_client.py contract.json
   python code_generator_server.py contract.json
   ```

3. **Running the Application:**
   ```bash

   python rpc_server.py
   

   python client.py
   ```

## System Architecture

### Components
1. **Code Generators**
   - `code_generator_client.py`: Generates client-side RPC stubs
   - `code_generator_server.py`: Generates server-side RPC handler

2. **Contract Definition**
   - `contract.json`: Defines available remote procedures
   - Specifies procedure names, parameters, and return types

3. **Runtime Components**
   - `server_procedure.py`: Contains actual function implementations
   - `rpc_server.py`: Handles incoming RPC requests
   - `rpc_client.py`: Provides client-side function stubs

### Contract Format
```json
{
    "remote_procedures": [
        {
            "procedure_name": "foo",
            "parameters": [
                {
                    "parameter_name": "par_1",
                    "data_type": "int"
                }
            ]
        },
        {
            "procedure_name": "bar",
            "parameters": [
                {
                    "parameter_name": "par_1",
                    "data_type": "int"
                },
                {
                    "parameter_name": "par_2",
                    "data_type": "string"
                }
            ],
            "return_type": "int"
        }
    ]
}
```

### Communication Protocol
- Uses TCP sockets for reliable communication
- JSON-based message format
- Request format: `{"procedure": "name", "params": {key: value}}`
- Response format: `{"result": value}` or `{"error": "message"}`
