import datetime
import getpass

import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message

class PeriodicSenderAgent(Agent):
    class InformBehav(PeriodicBehaviour):
        async def run(self):
            print(f"PeriodicSenderBehaviour running at {datetime.datetime.now().time()}: {self.counter}")
            msg = Message(to=self.get("receiver_jid"))  # Instantiate the message
            msg.body = f"{self.initial_sum}"  # Set the message content

            self.initial_sum += 100
            
            await self.send(msg)
            print("Message sent!")

            if self.counter == 5:
                self.kill()
            self.counter += 1

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

        async def on_start(self):
            self.counter = 0
            self.initial_sum=100

    async def setup(self):
        print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = self.InformBehav(period=2, start_at=start_at)
        self.add_behaviour(b)


class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=30)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 30 seconds")
                self.kill()

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        self.add_behaviour(b)

async def main():
    receiveragent = ReceiverAgent('radusalex@xmpp.jp', 'Focabob(100)#')
    senderagent = PeriodicSenderAgent('agent1_radu_mas@xmpp.jp', 'Focabob(100)#')

    await receiveragent.start(auto_register=True)

    senderagent.set("receiver_jid", 'radusalex@xmpp.jp')  # store receiver_jid in the sender knowledge base
    await senderagent.start(auto_register=True)

    await spade.wait_until_finished(receiveragent)
    await senderagent.stop()
    await receiveragent.stop()
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())