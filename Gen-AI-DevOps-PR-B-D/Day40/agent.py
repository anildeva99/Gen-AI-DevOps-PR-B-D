
m vertexai.preview import reasoning_engines
from tools import sample_tool

agent = reasoning_engines.Agent(
            model="gemini-2.0-flash",
                tools=[sample_tool],
                    enable_automatic_tool_choice=True,
                    )

