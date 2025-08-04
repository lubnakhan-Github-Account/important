from typing import Any
from pydantic import BaseModel,Field
from agents import Agent,Runner, TResponseInputItem,input_guardrail,RunContextWrapper,GuardrailFunctionOutput,InputGuardrailTripwireTriggered,enable_verbose_stdout_logging
from dotenv import load_dotenv
import rich

load_dotenv()
# enable_verbose_stdout_logging()
# --------------------------------------------
class Flight_checker(BaseModel):
    is_available:bool =Field(description="If user ask PIA flights insert false in this field.")
    # tickets:int =Field(default= 0,
    # description="if user wants any airline tickets deny and reply only availabel tickets of PIA  airline")
#-------------------------------------------------------------------------------------------------
guardrail_agent= Agent(
     name="guardrail_agent",
    instructions="you check if user ask PIA or not.",
    model="gpt-4.1-mini",
    output_type=Flight_checker,    
)
    

@input_guardrail
async def flight_guard(ctx :RunContextWrapper ,agent:Agent, input:str|list[TResponseInputItem])->GuardrailFunctionOutput:
    
  flight_result= await Runner.run(guardrail_agent, input,context=ctx)
  
  return GuardrailFunctionOutput(
      output_info=flight_result.final_output,
      tripwire_triggered=flight_result.final_output.is_available
      
     )
# -----------------------------------------------------------------------------------------
second_guardrail_agent= Agent(
    name="second_guardrail_agent",
    instructions="If user about another flight, additionally tell PIA airline.must run flight_guard input guardrail.",
    model="gpt-4.1-mini",
    input_guardrails=[flight_guard],
    handoff_description="You tell about user flights ."
)
      
triage_agent = Agent(
    name="triage_agent",
    instructions="you are a helpfull assistent.",
    model="gpt-4.1-mini",
    input_guardrails=[flight_guard],
    handoffs=[second_guardrail_agent]
    
) 
    
try :    
   result= Runner.run_sync(starting_agent=triage_agent,input="I want tickets of Emirates airline , call second_guardrail_agent.")
   rich.print(result.final_output) 
    
except  InputGuardrailTripwireTriggered as e :   
   print("❌", e)
    
    

