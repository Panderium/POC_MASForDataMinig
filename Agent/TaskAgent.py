#!/usr/bin/python3
import time
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template


class TaskAgent(Agent):            
    class ClassificationRequest(OneShotBehaviour):
        async def on_start(self):
            seekClassifier = Message("connection_agent@localhost")
            seekClassifier.set_metadata("performative", "ask")
            seekClassifier.set_metadata("ontology", "seek_classifier")
            await self.send(seekClassifier)
            
           

        async def run(self):
            msg = await self.receive(10)
            if msg:
                print("classification...")
                database = msg.get_metadata("database")
                self.agent.userAgent = str(msg.sender).split("/")[0]
                #Communique avec le classifier et fait remonter les données ou USER
                
                await asyncio.sleep(3)
                if self.agent.classifierList:
                    for agent in self.agent.classifierList:
                        message = Message(agent, "task_agent@localhost", database)
                        message.set_metadata("performative", "predict")
                        message.set_metadata("ontology", "classification")
                        await self.send(message)
                

            
    
    # class ClusteringRequest(OneShotBehaviour):

    #     async def run(self):
    #         msg = await self.receive(10)
    #         if msg:
    #             print("clustering...")
    #             database = msg.get_metadata("database")

    class ConnectionRespond(CyclicBehaviour):
        async def run(self):
            response = await self.receive()
            if response:
                if response.get_metadata("ontology") == "classification":
                    for classifier in response.body.split():
                        self.agent.classifierList.append(classifier)


    class ClassifierResponse(CyclicBehaviour):
        async def run(self):
            response = await self.receive()
            if response:
                message = Message(self.agent.userAgent, "task_agent@localhost", response.body)
                message.set_metadata("performative", "response")
                message.set_metadata("ontology", "classification")
                await self.send(message)

    
    
    async def setup(self):
        templateClass = Template()
        templateClass.set_metadata("performative", "request")
        templateClass.set_metadata("ontology", "classification")
        templateClustering = Template()
        templateClustering.set_metadata("performative", "request")
        templateClustering.set_metadata("ontology", "clustering")
        templateConnection = Template()
        templateConnection.set_metadata("performative", "response_connection")
        templateClassifier = Template()
        templateClassifier.set_metadata("performative", "classification_result")

        self.classifierList = list()
        self.userAgent = str()
        
        self.add_behaviour(self.ConnectionRespond(), templateConnection)
        self.add_behaviour(self.ClassificationRequest(), templateClass)
        self.add_behaviour(self.ClassifierResponse(), templateClassifier)
        #self.add_behaviour(self.ClusteringRequest(), templateClustering)
        


    