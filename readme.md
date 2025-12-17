Perfect — let’s walk through building a **FastMCP server** with a simple temperature conversion tool, exposing it over **HTTP transport**, and then connecting it in **AI Toolkit for VS Code**.  

---

## 🛠 Step 1: Project Setup
1. Create a new folder, e.g. `FastMCP.SimpleDemo`.
2. Initialize a Python environment:

```PowerShell
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install fastmcp
```
3. Check fastmcp version
```PowerShell
fastmcp --version
```
`output:`

``` text
FastMCP version:                                                                     2.14.0
MCP version:                                                                         1.24.0
Python version:                                                                      3.11.9
Platform:                                                         Windows-10-10.0.26100-SP0
FastMCP root path: C:\Users\ch15p\AppData\Local\Programs\Python\Python311\Lib\site-packages
```
---

## 🌡 Step 2: Define the Temperature Conversion Tool
FastMCP lets you define tools that can be exposed to AI agents.  
Here’s a simple tool for Celsius ↔ Fahrenheit conversion:

```python
# my_server.py

from fastmcp import FastMCP

mcp = FastMCP("Temp Conversion MCP Server")

@mcp.tool
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

@mcp.tool
def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

if __name__ == "__main__":
    # Expose via HTTP transport
    #mcp.run(host="0.0.0.0", port=8000)
    mcp.run(transport="http", port=8000)
```

---

## 🌐 Step 3: Run the Server
Start your server:
```PowerShell
fastmcp run tempconversion-mcp-http.py:mcp --transport http --port 8000
```
`output:`

```text
╭──────────────────────────────────────────────────────────────────────────────╮
│                                                                              │
│                         ▄▀▀ ▄▀█ █▀▀ ▀█▀ █▀▄▀█ █▀▀ █▀█                        │
│                         █▀  █▀█ ▄▄█  █  █ ▀ █ █▄▄ █▀▀                        │
│                                                                              │
│                                FastMCP 2.14.0                                │
│                                                                              │
│                                                                              │
│                  🖥  Server name: Temp Conversion MCP Server                 │
│                                                                              │
│                  📦 Transport:   HTTP                                        │
│                  🔗 Server URL:  http://127.0.0.1:8000/mcp                   │
│                                                                              │
│                  📚 Docs:        https://gofastmcp.com                       │
│                  🚀 Hosting:     https://fastmcp.cloud                       │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
[12/14/25 11:19:02] INFO     Starting MCP server 'Temp Conversion MCP Server' with transport 'http' on                server.py:2582
                             http://127.0.0.1:8000/mcp                                                                              
INFO:     Started server process [26956]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
It will listen on `http://localhost:8000/mcp`.

---

## 🔗 Step 4: Connect via AI Toolkit in VS Code
1. Open **VS Code** with the **AI Toolkit extension** installed.
2. Go to **AI Toolkit → MCP Servers → Add Server**.
3. Choose **HTTP transport**.
4. Enter:
   - **Name**: `Temp Conversion MCP`
   - **URL**: `http://localhost:8000/mcp`
5. Save and connect.

Now, your AI Toolkit can call `celsius_to_fahrenheit` and `fahrenheit_to_celsius` directly as MCP tools.

---
## ✅ Step 5: Test with VS Code > mcp.json

- Add `.vscode\mcp.json` file at the root of the project and add following content in it.

```json
{
    "servers": {
        "my-fastmcp-server": {
            "type": "http",
            "url": "http://127.0.0.1:8000/mcp"            
        }
    }
}
```
- Use MCP tools command from mcp.json to start / stop / restart fastmcp server

## ✅ Step 6: Test in AI Toolkit
- Open the AI Toolkit chat.
- Type:  
  ```
  Use the Temp Conversion MCP server to convert 100 Celsius to Fahrenheit.
  ```
- The tool should respond with `212.0`.

---

let’s add a **manifest file (`mcp.json`)** so your FastMCP server can be auto-discovered by AI Toolkit in VS Code.  

---

## 📄 Step 6: Create `mcp.json`
In your project root (`fastmcp-temp-server`), add a file named `mcp.json`:

```json
{
  "name": "Temp Conversion MCP",
  "version": "1.0.0",
  "description": "A simple FastMCP server for temperature conversion tools.",
  "transport": {
    "type": "http",
    "url": "http://localhost:8000"
  },
  "tools": [
    {
      "name": "celsius_to_fahrenheit",
      "description": "Convert Celsius to Fahrenheit",
      "input_schema": {
        "type": "object",
        "properties": {
          "celsius": { "type": "number" }
        },
        "required": ["celsius"]
      },
      "output_schema": {
        "type": "number"
      }
    },
    {
      "name": "fahrenheit_to_celsius",
      "description": "Convert Fahrenheit to Celsius",
      "input_schema": {
        "type": "object",
        "properties": {
          "fahrenheit": { "type": "number" }
        },
        "required": ["fahrenheit"]
      },
      "output_schema": {
        "type": "number"
      }
    }
  ]
}
```

---

## 📂 Step 8: Place the Manifest
- Save `mcp.json` in the **same folder** as your `server.py`.
- AI Toolkit will look for this manifest when you add the server.

---

## 🔗 Step 9: Connect in AI Toolkit
1. Open VS Code → AI Toolkit.
2. Go to **MCP Servers → Add Server → Import from Manifest**.
3. Select your `mcp.json`.
4. AI Toolkit will auto-register the server with the tools defined.

---

## ✅ Step 10: Test
- In AI Toolkit chat, try:
  ```
  Convert 0 Celsius to Fahrenheit using Temp Conversion MCP.
  ```
- It should return `32.0`.

## 🔗 References

[FastMCP](https://gofastmcp.com/getting-started/welcome)

[FastMCP Quickstart](https://gofastmcp.com/getting-started/quickstart)

[How to Create an MCP Server in Python](https://gofastmcp.com/tutorials/create-mcp-server)

[FastMCP Cloud](https://fastmcp.cloud/)
