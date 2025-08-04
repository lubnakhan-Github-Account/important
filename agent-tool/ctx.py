from agents import Agent, RunContextWrapper, Runner, function_tool, set_tracing_disabled,OpenAIChatCompletionsModel,AsyncOpenAI

import os 
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
# local / llm ctx with pydentic object.

class Book_info(BaseModel):
    bookName:str
    author:str
    publishYr:int
    genre:str
    
about_book =  Book_info( bookName="Harry Potter",author="JK Rowling",publishYr=2003,genre= "fantasy")   

def dynamic_instrections(wrapper:RunContextWrapper[Book_info],agent:Agent[Book_info]):
    wrapper.context.bookName="GoodBye"
    return f"when user ask about book use given tool favorite_book to get genre, author and bookName.book name is{wrapper.context.bookName} publishYr is{wrapper.context.publishYr}."
    
@function_tool
def favorite_book(wrapper:RunContextWrapper[Book_info]):
    return f"The genre is {wrapper.context.genre} the author is {wrapper.context.author}"
    

client= AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

agent= Agent[Book_info](
    name="my_agent",
    instructions=dynamic_instrections,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash-lite",openai_client=client),
    tools=[favorite_book]
)
result= Runner.run_sync(agent, "what is bookName, author ,publishYr  and genre of favorite book?",context=about_book)
print(result.final_output)
