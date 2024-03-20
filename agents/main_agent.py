import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour,CyclicBehaviour
from agents.small_agent import SmallAgent
from constants import *
from spade.message import Message

class MainAgent(Agent):
    class ReceiveCards(CyclicBehaviour):
        async def run(self):
            self.jid = self.get('main_jid')
            msg = await self.receive(timeout=10)
            
            if int(self.get('life'))<=0:
                msg = Message(to = AGENT2_JID)
                msg.body = 'lost'
                await self.send(msg)
                
                msg = Message(to = AGENT3_JID)
                msg.body = 'lost'
                await self.send(msg)
                
                self.kill()
                self.agent.stop()
            
            if msg :
                small_agent_power = int(msg.body)
                
                if random.randint(2,14) > small_agent_power:
                    msg = Message(to = msg._sender.localpart+'@'+msg._sender.domain)
                    msg.body = "0" 
                    await self.send(msg)
                else:
                    msg = Message(to = msg._sender.localpart+'@'+msg._sender.domain)
                    msg.body = "1"
                    life = self.get('life')
                    print(f'{bcolors.OKBLUE}{self.get("main_jid")} - {self.get("life")}{bcolors.ENDC}')
                    life = life - small_agent_power
                    self.set('life',life)
                    print(f'{bcolors.OKBLUE}{self.get("main_jid")} - {self.get("life")}{bcolors.ENDC}')
                    await self.send(msg)
            else:
                print(f"{self.get('main_jid')} - {self.get('life')}")
                self.kill()
                
        async def on_end(self):
            await self.agent.stop()
            
    async def setup(self):
        print(f"Main Agent {self.jid} created.")
        self.set('main_jid',self.jid)
        self.set('life',200)
        b = self.ReceiveCards()
        self.add_behaviour(b)

class CreateBehav(OneShotBehaviour):
    async def run(self):
        smallagent1 = SmallAgent(AGENT2_JID, get_password())
        smallagent2 = SmallAgent(AGENT3_JID, get_password())
        
        await smallagent1.start(auto_register=True)
        await smallagent2.start(auto_register=True)