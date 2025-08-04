from dataclasses import dataclass
import os
from agents import Agent, RunContextWrapper,Runner, function_tool,set_tracing_disabled,OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)
# -----------------------------------------------------
# ctx with data class
# -----------------------------------------------------

@dataclass
class User:
    name:str
    age:int
    id:int
    
user_info= User("John",12,990087)
# -----------------------------------------------
# llm-ctx via function tool for llm.
@function_tool
def local_func(wrapper:RunContextWrapper[User]):
    """this is instrections, only segnature, doc str 
    and parameter are go to agent through function tool in json schema.
    here we also create a dataclass to pass schema/ object.
    """
    return f"{wrapper.context.id} {wrapper.context.age}"


# -----------------------------------------------
#  local-ctx here we give dynamic instractions via function.
def dynamic_ins(wrapper: RunContextWrapper[User], agent:Agent)->str:
    return f" when user ask about name, age and id you call given local_func tool.my name is {wrapper.context.name} {wrapper.context.age} {wrapper.context.id}."
# ---------------------------------------------------------
client= AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent= Agent[User](
    name="local agent",
    instructions=dynamic_ins,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite", openai_client=client),
    tools=[local_func]
)

result= Runner.run_sync(agent,"what is user name ,age and id.", context=user_info)
print(result.final_output)