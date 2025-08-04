from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,handoff, Handoff,function_tool
from dotenv import load_dotenv
from agents.extensions import handoff_filters
import rich
from agents import enable_verbose_stdout_logging
from pydantic import BaseModel

load_dotenv()
enable_verbose_stdout_logging()
# -----------------------------------------------
def greet():
    return "hello"
   
        
# handoff-description m(what is does / when to invoke it.)as a/b(wo kia krta h or kb chalana h) 
surgeon_agent= Agent(
    name="surgeion_agent",
    instructions="you are an expert surgeon and handle all users as a patient.",
    handoff_description="you do advise  to user when they tell you query .",
)
# ----------------------------------------------------------------------------
doctor_agent=  handoff(
    agent=surgeon_agent,
    tool_name_override="dentist_agent",
    tool_description_override="you  are good doctor and reply in short way .",
    
    input_filter=handoff_filters.remove_all_tools
)
    

agent = Agent(
    name="triage_agent",
    instructions=" alwayes use tool before reply,you are a helpful assistent.",
    model="gpt-4.1-mini",
    handoffs=[doctor_agent],
    tools=[greet]
)

result= Runner.run_sync(agent,"i have pain in my tooth.")
rich.print("✅",result.final_output)
print(result.last_agent)

