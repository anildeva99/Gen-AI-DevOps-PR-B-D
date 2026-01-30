from vertexai.generative_models import FunctionDeclaration, Tool
import json

# -------------------------------
# Tool 1: add_numbers
# -------------------------------
def add_numbers(a: int, b: int) -> int:
    return a + b

add_numbers_decl = FunctionDeclaration(
    name="add_numbers",
    description="Adds two numbers",
    parameters={
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"}
        },
        "required": ["a", "b"]
    }
)

# -------------------------------
# Tool 2: say_hello
# -------------------------------
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

say_hello_decl = FunctionDeclaration(
    name="say_hello",
    description="Returns a greeting",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
)

# -------------------------------
# Tool Container
# -------------------------------
tools = Tool(function_declarations=[
    add_numbers_decl, 
    say_hello_decl
])

# -------------------------------
# Tool execution router
# -------------------------------
def execute_tool(name: str, arguments: dict):
    if name == "add_numbers":
        return add_numbers(arguments["a"], arguments["b"])
    if name == "say_hello":
        return say_hello(arguments["name"])
    return "Unknown tool"

