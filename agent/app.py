from agents import Agent, Model,Runner,function_tool,enable_verbose_stdout_logging,ModelSettings
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal
import rich
# enable_verbose_stdout_logging()


load_dotenv()
# -------------------------------------
class  Book_appointment(BaseModel):
    is_appointment:bool = Field(description="if user ask about appointment use confrim_appoint tool.")
    status:Literal["confrimed","canciled",None] =Field(description="if user query is not related Literal value,keep the value is None.")
    day:str =Field(description="saturday,sunday")
# ===========================================================================================
@function_tool(is_enabled=True)
def confrim_appoint(book:Book_appointment)->str:
    """Book the the appointment confrimed"""
    return f"I m John my appointment is {book.status} at the {book.day}"
# ==================================================================================
# doctor_agent = Agent(
#     name="doctor_agent",
#     instructions="you are a doctor agent.",
#     model="gpt-4.1-mini",
#     handoff_description="you solve qury of user about health issue."
# )
    

agent= Agent(
    name="main_agent",
    instructions="when user ask about appointment use tool and don't reply yourself, and confrim_appoint is True then handoffs it doctoe_agent.",
    model="gpt-4.1-mini",
    output_type=Book_appointment,
    model_settings=ModelSettings(tool_choice="required"),
    tools=[confrim_appoint],
    # handoffs=[doctor_agent]
    
)
result= Runner.run_sync(agent,"I book my appointment on sunday.")
rich.print(result.final_output)
# print(result.last_agent)

print("============================================================")


if result.final_output.is_appointment == True:
    rich.print(f"Mr. John your  appointment is {result.final_output.status} at the {result.final_output.day}")
    




