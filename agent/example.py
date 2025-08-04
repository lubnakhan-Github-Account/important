from dataclasses import dataclass
from typing import Awaitable

@dataclass
class Agent1():
    name:str ="abc"  # field / dataclass init ka function khud bnati h.bnana nhi prta.
                #dataclass m field ko igr default value dein gy
                # tou wo is attribute ko class level or instance level dono p bnati h
# default value nhi dein gy tou wo init ka function bna dygi or self s value get ho jaye gi or 


class Agent():
   def __init__(self,name):
      name :str = self.name 
# =======================================================================
# tool_choise loop ko rokne ka parameter h
# Model setting ki class k parameter h tool_choise.


# ================================================Awaitable
async def addition(a:str,b:str)-> Awaitable(str): # type: ignore #igr ye async function
                                             #  ho or koi async call kra rahe hon tou ye  
   return  await "abc"                        #return string tou h but ye Awaitable string h.  
