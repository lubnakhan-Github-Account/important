from dotenv import load_dotenv
from agents import Agent, Runner, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, WebSearchTool,input_guardrail
import rich
from pydantic import BaseModel, Field
# -----------------------------------------
load_dotenv()
# -----------------------------------------
class Prime_Minister_Check(BaseModel):
    is_prime_minister: bool = Field(instruction="check if user is asking about prime minister so insert True in this field.")
# -----------------------------------------
guardrail_agent = Agent(
    name="guardrail_agent",
    instructions="check if user is asking about prime minister",
    output_type=Prime_Minister_Check,
    model="gpt-4.1-mini",
    handoff_description=""
)
# -----------------------------------------
@input_guardrail
async def prime_minister(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem])-> GuardrailFunctionOutput:
    
    guard_output = await Runner.run(guardrail_agent, input, context=ctx)

    return GuardrailFunctionOutput  (
        output_info = guard_output.final_output,
        tripwire_triggered =guard_output.final_output.is_prime_minister,
    )
# -----------------------------------------
agent = Agent(
    name="triage_agent",
    instructions="you are a helpful assistant",
    model="gpt-4.1-mini",
    input_guardrails=[prime_minister],
    handoffs=[guardrail_agent]
    )
# -----------------------------------------
try:
    result = Runner.run_sync(agent,  input="hi, who is the prime minister of Pakistan")
    rich.print(result.final_output)
except InputGuardrailTripwireTriggered as e:
    print("❌", e)