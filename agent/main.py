from agents import Agent, Runner, set_tracing_disabled,function_tool, ModelSettings, RunContextWrapper,FunctionTool
from agents.agent import StopAtTools
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any

load_dotenv()
# -------------------------------------------------------for custom tool
def do_some_work(data:str)-> str:
    return "done"

class FunctionArgs(BaseModel):
    username:str
    age:int
    
async def run_function(ctx:RunContextWrapper[Any],args:str)->str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")
   
tool = FunctionTool(
    name="process user",
    description="this is custom tool ",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
) 
#---------------------------------------------------------------------      
     













class Addparam(BaseModel):
    a:int |str
    b:int

# @function_tool(strict_mode=True)
# def add(params: Addparam) ->int:
#     """Add two numbers"""
#     return params.a + params.b
    

@function_tool(name_override="addition",description_override="we change description too")  #is parameter s name ko change krskty h.
def add(a:int | str, b:int)-> int:
    """Add two numbers."""
    print("add called")
    return a+b -5

@function_tool()  #ye is func ko call kr raha h
def human_review():
    """human in the loop interface """
    print("function human review called")
    return "human in the loop called"


agent = Agent(
    name= "custom_agent",
    instructions="This is an example agent that does nothing special.",
    tools=[add,human_review],
    
    # tool_use_behavior="stop_on_first_tool" # ye 1st tool k return ko
    # final output bna dega means answer.ye llm k pass nhi jaye ga.
    #  tool_use_behavior=StopAtTools(stop_at_tool_names=["human_review"]),
    #  model_settings=ModelSettings(tool_choice="required"),
    #  reset_tool_choice=False 
     # 10 br chalye ga phr MaxTurnsExceeded ka error aye ga.
    
    # model="gpt-4.1-mini"
    
)
print(agent.tools)

# result = Runner.run_sync(starting_agent=agent,input="2 plus 2 =?")
# #Runner loop ko modify krskty h.or final output llm nhi, tool bhi dey skta h
# print(result.final_output)
