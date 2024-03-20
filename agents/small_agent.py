import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour,PeriodicBehaviour
from constants import *
from spade.message import Message

class SmallAgent(Agent):
    class PickCard(PeriodicBehaviour):
        async def run(self):
            msg = Message(to = self.get('main_agent_jid'))
            
            self.cards = self.get('cards')
            self.jid = self.get('self_jid')
            
            msg.body = str(self.cards.pop(0))
            
            print(f'{self.jid} - picks a card - {msg.body}')
            
            random.shuffle(self.cards)
            self.set('cards',self.cards)
            
            print(f'{self.jid} - cards left: {self.cards}')
            
            await self.send(msg)
            
            if(len(self.cards)==0):
                self.kill()
    
    class ReceiveCards(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)

            if msg:
                if msg.body == 'lost':
                    self.kill()
                    await self.agent.stop()
                    print(f'{bcolors.OKGREEN}the main agent lost{bcolors.ENDC}')
                else:
                    if type(int(msg.body)) is int:
                        print(f'{self.get("self_jid")} - received status: {msg.body}')
                        winnings = self.get('winning')
                        winnings = winnings + int(msg.body)
                        self.set('winning',winnings)
            else:
                self.kill()
                print(f"{self.get('self_jid')} - {self.get('winning')}")
                
        async def on_end(self):
            await self.agent.stop()
            
    async def setup(self):
        self.main_jid = AGENT1_JID
        
        self.cards:list = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        random.shuffle(self.cards)
        
        self.set('cards',self.cards)
        self.set('main_agent_jid',self.main_jid)
        self.set('self_jid',self.jid)
        self.set('winning',0)
                
        print(f"Small agent {self.jid} created. {self.cards}")
        b = self.PickCard(period=2)
        self.add_behaviour(b)
        
        a = self.ReceiveCards()
        self.add_behaviour(a)