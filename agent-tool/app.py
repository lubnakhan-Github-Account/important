import asyncio
import os
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled,RunContextWrapper
from dotenv import load_dotenv
import rich
from pydantic import BaseModel


load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

client= AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
 )
class Student(BaseModel):
    name:str
    roll_no:int
    

st_name= input('Enter name: ')
st_roll_no= input('Enter roll_no: ')

std= Student(name=st_name,roll_no=st_roll_no)

def dyn(wrapper:RunContextWrapper[Student] ,agent):
    return f"name is {wrapper.context.name} roll number is {wrapper.context.roll_no}"

agent = Agent(
    name="z_agent",
   instructions= dyn,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite",openai_client=client),
)



# async def main():
#    my_name="jackson"
#    custom_ctx=RunContextWrapper(context=my_name)    # ok
   
#    res = await agent.get_system_prompt(custom_ctx)
#    print("✅",res) 
   
#    result= await Runner.run(agent,"hi", context=my_name)
#    rich.print(result)
#    print("\n")
#    print(result.final_output)

# asyncio.run(main())

result=  Runner.run_sync(agent,"what is student name and roll number.", context=std)
rich.print(result)
print("\n")
print(result.final_output)