import random
import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour,CyclicBehaviour,PeriodicBehaviour
from agents.main_agent import CreateBehav, MainAgent
from constants import *
from spade.message import Message


async def main():
    main_agent = MainAgent(AGENT1_JID, get_password())
    behav = CreateBehav()
    main_agent.add_behaviour(behav)
    await main_agent.start(auto_register=True)
    
    # wait until the behaviour is finished to quit spade.
    await behav.join()
    
    print("Agents finished")

if __name__ == "__main__":
    spade.run(main())