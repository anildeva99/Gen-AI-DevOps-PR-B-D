from vertexai.preview import tool

@tool
def ping_server(server_name: str) -> str:
    """Simulates pinging a server."""
    return f"Server '{server_name}' is reachable."

@tool
def check_cpu(server_name: str) -> str:
    """Simulates CPU check."""
    return f"CPU usage on {server_name} is 45%."

