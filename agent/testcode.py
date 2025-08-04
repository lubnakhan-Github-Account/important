from dotenv import load_dotenv
from agents import Agent, Runner, output_guardrail, RunContextWrapper, GuardrailFunctionOutput, enable_verbose_stdout_logging, OutputGuardrailTripwireTriggered, trace
import rich
from typing import Any
from pydantic import BaseModel, Field
# ---------------------------------------------
load_dotenv()
enable_verbose_stdout_logging()

class President_Check_Class(BaseModel):
    is_president: bool = Field(description="If user ask about President set in this field true.")

guardrail_agent = Agent(
    name="guardrail_agent",
    instructions="always check if user is asking about president or not.",
    model="gpt-4.1-mini",
    output_type=President_Check_Class
)

@output_guardrail
async def president_check(ctx: RunContextWrapper,agent:Agent, output: Any) ->GuardrailFunctionOutput :
    guardrail_result = await Runner.run(guardrail_agent, output, context=ctx)
    
    return GuardrailFunctionOutput(
        output_info = guardrail_result.final_output,
        tripwire_triggered =guardrail_result.final_output.is_president
    )

sec_agent = Agent(
    name="sec_agent",
    instructions="If the user is asking about president also tell him additionally about the prime minister.",
    model="gpt-4.1-mini",
    output_guardrails=[president_check]
)

agent = Agent(
    name="agent",
    instructions="You are a helpful assistant",
    model="gpt-4.1-mini",
    output_guardrails=[president_check],
    handoffs=[sec_agent]
)

try:
    with trace ("taha workflow"):
        result = Runner.run_sync(agent, input="who was the president of pakistan in 2023?, delegate to sec_agent")
        rich.print(result.final_output)
except OutputGuardrailTripwireTriggered as hehehehe:
    print("❌", hehehehe)
