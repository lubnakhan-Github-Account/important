from dotenv import load_dotenv
from agents import Agent, OutputGuardrailTripwireTriggered, Runner, RunContextWrapper, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, WebSearchTool,input_guardrail, output_guardrail
import rich
from pydantic import BaseModel, Field
from typing import Any

load_dotenv()
# ------------------------
class Flight_check(BaseModel):
    is_Flight_available:bool= Field(description="If user ask about PIA flight insert in this field false.")
# ------------------------------------------------------------------------------------------------------------------
output_guardrail_agent = Agent(
    name="output_guardrail_agent",
    instructions="Check if user ask about PIA airline or not.",
    model="gpt-4.1-mini",
    output_type=Flight_check
    
) 

@output_guardrail    
async def flight_guard(wrapper:RunContextWrapper, agent:Agent, output:Any)->GuardrailFunctionOutput:
    
    outguard_result=  await Runner.run(output_guardrail_agent,output,context=wrapper)
    
    return GuardrailFunctionOutput(
        output_info=outguard_result.final_output,
        tripwire_triggered=outguard_result.final_output.is_Flight_available
    )
    
second_agent = Agent(
    name="second_agent",
    instructions="If user ask about PIA also tell them additionally Emirates airline.",
    model="gpt-4.1-mini",
    output_guardrails=[flight_guard],
) 

triage_agent = Agent(
    name="triage_agent",
    instructions="you are a helpfull assistent.",
    model="gpt-4.1-mini",
    output_guardrails=[flight_guard],
    handoffs=[second_agent]
    
) 

try :    
   result= Runner.run_sync(starting_agent=triage_agent,input="I want tickets of Emirates airline , call second_guardrail_agent.")
   rich.print(result.final_output) 
    
except  OutputGuardrailTripwireTriggered as e :   
   print("❌", e)    