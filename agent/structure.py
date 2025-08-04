from pydantic import BaseModel, Field

from agents import Agent,Runner
import rich
from dotenv import load_dotenv

load_dotenv()

class about_me(BaseModel):
    is_name:bool = Field(description="if user ask name must return true or false.") 
    name:str
    age:int= Field(default=None, gt=0,description="user age is not given")


agent = Agent(
    name="triage_agent",
    instructions="you are a helpfull assistent. ",
    model="gpt-4.1-mini",
    output_type=about_me
)

result= Runner.run_sync(agent,"my name is John .")
rich.print(result.final_output)
# -------------------------------------------------------
print("============================================")
if result.final_output.is_name == True:
    if result.final_output.name:
        print(f"hi 👋 {result.final_output.name} how are you.")
    if result.final_output.age > 0:
        print(f"you are {result.final_output.age} years old.")    