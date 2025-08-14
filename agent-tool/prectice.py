from dataclasses import dataclass
import os
from agents import Agent, ModelSettings, RunContextWrapper,Runner, function_tool, set_tracing_disabled,OpenAIChatCompletionsModel,AsyncOpenAI
from dotenv import load_dotenv
from agents.agent import StopAtTools
load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)
# -----------------------------------------
client= AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
 )
# @function_tool
# def weather(city:str)->str:
#     return f"The weather in {city} is sunny"

# ---------------------------------------------------
# @function_tool
# def karachi_weather(city:str):
#     return f"The weather of {city} is hot."
# ------------------------------------------------dynamic instrections/ system prompt
@dataclass
class User:
    name:str
    ph:str
    current_conversation: list[str]
    
def get_memory(self):
    return f"user {self.name} has a ph no {self.ph} "

def update_memory(self,memory: str):
    self.memory = memory
    
def update_conversation(self, message:str):
    self.current_conversation.append(message)    
        
        
async def get_system_prompt(ctx:RunContextWrapper[User],agent:Agent[User]):
    print("\n[context]",ctx.context)
    print("\n[agent]" ,agent)
  
    # ctx.context.update_memory(f"user {ctx.context.name}  has ph no {ctx.context.ph}")
    ctx.context.update_conversation(f"user {ctx.context.name} has a ph no {ctx.context.ph}")
    
    return f"you are a helpful assistent that can help with task."

# ---------------------------------------------------------------------------------

user_1= User(name="Ameen Alam",ph="0987654",current_conversation=[])

agent = Agent(
    name="Haiku-agent",
    instructions=get_system_prompt,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite",openai_client=client),
    # tools=[karachi_weather,weather],
    #  tool_use_behavior=StopAtTools(stop_at_tool_names=["karachi_weather"]),
    # tool_use_behavior="stop_on_first_tool",
    # model_settings=ModelSettings(tool_choice=None,parallel_tool_calls=False),
    # reset_tool_choice=True,
)

    
    
# result= Runner.run_sync(starting_agent=agent, input="what is the weather of karachi.", max_turns=1)
# print(result.final_output)
result= Runner.run_sync(agent,"hi",context=user_1)
print(result.final_output)
print(user_1.get_memory()) #not ok (remove max_turns before file run) 
