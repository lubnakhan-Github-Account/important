from agents import Agent,Runner, enable_verbose_stdout_logging,handoff,Handoff,RunContextWrapper
from agents.extensions import handoff_filters
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
enable_verbose_stdout_logging()
# ---------------------------------------
surgeon_agent= Agent(
    name="surgeion_agent",
    instructions="you are an expert surgeon and handle.Provide clear information about diseses.",
    handoff_description="you support user in surgery issues."
    # handoff_description="you do advise  to user when they tell you query .",
)
dentest_agent= Agent(
    name="dentest_agent",
    instructions="you are an expert doctor.Assist user in their qurey.",
    handoff_description="you handel dentail issues.",
    model="gpt-4.1-mini",
    # handoff_description="you do advise  to user when they tell you query .",
)
class HandMod(BaseModel):
    input :str


handmad= HandMod.model_json_schema()
handmad["additionalProperties"] =False
# -------------------------------------------
async def func_invoke(ctx:RunContextWrapper, input:str):
    
    # print("input:",input)
    return dentest_agent
# ----------------------------------------------------------
def enable_func(context:RunContextWrapper,agent:Agent):
    return True


dentest_agent_handoff=  Handoff(
      tool_name="dentest_agent",
      tool_description="you support user in  health issues.",
      input_json_schema=handmad,
      on_invoke_handoff=func_invoke,
      agent_name="dentest_agent",
      is_enabled=enable_func,
      strict_json_schema= True,
    # tool_name_override="dentist_agent",
     input_filter=handoff_filters.remove_all_tools
)
agent= Agent(
    name="triage_agent",
    instructions="you delegate task to apropriate agent.",
    model="gpt-4.1-mini",
    handoffs=[surgeon_agent,dentest_agent_handoff]
)
result= Runner.run_sync(agent,"hi,i have some tooth issue.")
print("♦✅",result.final_output)


    



