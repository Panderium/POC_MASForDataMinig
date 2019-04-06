#!/usr/bin/python3
import time
import sys
import asyncio
from Agent.TaskAgent import TaskAgent
from Agent.Utils import formMessage, parseRequest
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from spade.message import Message


class UserAgent(Agent):  
    class ReceiveTaskResponse(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                if msg.get_metadata("ontology") == "classification":
                    accurancy, classifier = msg.body.split()
                    print("La précision de la classificaion est de {} avec le classifier {}.".format(accurancy, classifier))
                    await self.agent.taskAgent.stop()
                    await self.agent.stop()  


    class NewTaskBehaviour(OneShotBehaviour):    
        async def on_start(self):
            print("Bienvenue")
            self.message = Message()
            
            
        async def run(self):
            while True:
                request = input("Quelle tâche de data mining voulez-vous lancer ?\n")
                self.wellFormedRequest = parseRequest(request)
                if self.wellFormedRequest != 1:
                    break

            self.agent.taskAgent = TaskAgent("task_agent@localhost", "taskAgent")
            await self.agent.taskAgent.start()
            self.agent.taskAgent.web.start("127.0.0.1", "10003")
            self.message = formMessage(str(self.agent.jid), str(self.agent.taskAgent.jid), "request", self.wellFormedRequest[0], {"database" : self.wellFormedRequest[1]})
            await self.send(self.message)
                        

    
    async def setup(self):
        print("User agent starting...")
        template = Template()
        template.set_metadata("performative", "response")
        self.add_behaviour(self.NewTaskBehaviour())
        self.add_behaviour(self.ReceiveTaskResponse(), template)

if __name__ == "__main__":
    userAgent = UserAgent("user_agent@localhost", "userAgent")
    userAgent.start()
    userAgent.web.start("127.0.0.1", "10000")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    userAgent.stop()



        