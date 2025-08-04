from datetime import datetime, time
from dotenv import load_dotenv
from agents import Agent,Runner,ModelSettings,function_tool,RunContextWrapper
from typing import Literal


load_dotenv()
# ===========================
# project seafood resturant.2nd module


def is_business_hours():
    now= datetime.now().time()
    business_start= time(20,0) 
    business_end= time(22,0)
    return (business_start <= now) and (now <= business_end)
# =================================================================
def closed_tool_switcher(ctx:RunContextWrapper, agent:Agent)->bool:
    """enable shop_closed tool only when shop is closed"""    
    return not is_business_hours()

def rice_tool_switcher(ctx:RunContextWrapper, agent:Agent)->bool:
    if ctx.context.order_type == "rice":
       return True
    return False

def fish_tool_switcher(ctx:RunContextWrapper, agent:Agent)->bool:
    if ctx.context.order_type == "fish":
       return True
    return False

# ===================================================
@function_tool(is_enabled=closed_tool_switcher)
def shop_closed()->str:
    """return shop closed notice"""
    return "shop is closed comeback during opening hours.(5:00pm to 11:00pm),your ordernot be placed yet. "
    
@function_tool(is_enabled=rice_tool_switcher)
def rice_order():
    """give update about rice order."""
    
    return "your rice is cooking wait for 3 minutes.⏰"

@function_tool(is_enabled=fish_tool_switcher)
def fish_order():
    """provide update about fish order."""
    
    return "your fish is cooking wait for 5 minutes.⏰"
# ========================================================================
order_agent =Agent(
    name="order_agent",
    instructions=""" First check timing to shop_closed tool if available.
    you are a order taker  manager of a fast food resturant,
    use tools that provided you ,do not guess always call tool.
    if shop closed ,used tool to notify.
    """,
    model="gpt-4.1-mini",
    tools=[fish_order, rice_order,shop_closed],

    model_settings=ModelSettings(temperature=0.3,tool_choice="required"),
    
)