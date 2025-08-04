from agents import Agent,Runner,ModelSettings,enable_verbose_stdout_logging
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from oder import order_agent

from typing import Literal
import rich
# enable_verbose_stdout_logging()
# project seafood resturant 1st module


load_dotenv()

class order_check(BaseModel):
    is_order:bool= Field(
        description="if user give an order use true, or not anorder use false. only reply about 'fish' and 'rice'. ")
    quantity:int=Field(default=0, description="user quantity set if not set 0")
    reason:str=Field(description="summerize the user qury in one sentance and do not reply if is not relavent the order.")
    order_type:Literal["fish","rice",None] =Field(description="set fish if order is fish or rice otherwise set None.")
    user_question:str=Field(description="copy the user question.")
    

main_agent =Agent(
    name="main_agent",
    instructions="you only handle order related query.",
    model="gpt-4.1-mini",
    output_type=order_check,
    
)
result= Runner.run_sync(main_agent,"Please make 2 fried Fishs with 1 plate rice.")
rich.print(result.final_output)

if result.final_output.is_order == True:
    
    my_order_agent= Runner.run_sync(order_agent,input=result.to_input_list(),context=result.final_output)
    rich.print('order agent:',my_order_agent.final_output)