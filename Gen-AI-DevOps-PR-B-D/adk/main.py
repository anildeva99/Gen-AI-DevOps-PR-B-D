from vertexai.preview.agent import Agent
from .tools import ping_server, check_cpu

# Create agent instance
agent = Agent.from_components(
    model="google/gemini-2.0-flash",
    system_instruction=open("agent/system_prompt.txt").read(),
    tools=[ping_server, check_cpu],
)

