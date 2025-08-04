import asyncio
from agents import Agent,Runner,set_tracing_disabled,OpenAIChatCompletionsModel,AsyncOpenAI, RunContextWrapper
import os
from dotenv import load_dotenv
import rich
from pydantic import BaseModel

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

client =AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
    
# ========================================================================
# this file has code for system prompt & dynamic instructions

def func(wrapper:RunContextWrapper,agent:Agent):
    return f" your name is uncal {wrapper.context}"


agent = Agent(
    name="z_agent",
    instructions=func, #yahn dynamic instruction di h(func)
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite",openai_client=client)
)

# ----------------------------------------------------------------------------- 
async def main():  #ye system prompt h us ko get krne k leye kia h ye 

   custom_ctx=RunContextWrapper(context="alexxx")
   res=  await agent.get_system_prompt(custom_ctx) # ye 1 method h jis se hm system prompt ko 
#    locally apne terminal p dekh skty hain.
   print("✅",res) #ye system prompt ka reply h terminal pr.
    


   output=   await Runner.run(agent,"hi", context=custom_ctx)
   rich.print(output)
   print(output.final_output)
   
asyncio.run(main())   