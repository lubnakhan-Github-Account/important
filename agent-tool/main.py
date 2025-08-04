from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

client= AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# code for agent as tool main.py
book_agent= Agent(
    name="triage_agent",
    instructions="you assist user about  books and give information.",
    handoff_description="book_agent to help user in inform about books.",
     model= OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite",openai_client=client)
)
flower_agent= Agent(
    name="flower_agent",
    instructions="you help in about the flowers.",
    handoff_description="flower_agent to help user in inform about flowers.",
     model= OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite",openai_client=client)
)

triage_agent= Agent(
    name="triage_agent",
    instructions="you are a triage_agent,you delegate task to appropriate agent or  given tools."
    "you never reply on your own,use tools",
    model= OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite",openai_client=client),
    tools=[
        book_agent.as_tool(
            tool_name="transfer_to_book_agent",
            tool_description="book_agent to help user in inform about books.start reply with this 📚 emoji."
        ),
        flower_agent.as_tool(
            tool_name="transfer_to_flower_agent",
            tool_description="flower_agent to help user in inform about flowers. start reply with this 🌺 emoji."
        ) 
    ]
    
    
)
result= Runner.run_sync(starting_agent=triage_agent, input="in which areas jasmeen flower are grow, and book cendrlla ." ,max_turns=2)
print(result.final_output)