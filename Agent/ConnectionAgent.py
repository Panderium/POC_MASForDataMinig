#!/usr/bin/python3
import time
import sys
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from spade.message import Message

class ConnectionAgent(Agent):
    class NewConnection(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                sender = str(msg.sender).split('/')
                sender = sender[0]
                if msg.get_metadata("ontology") == "new_classifier":
                    self.agent.classifierJID.append(sender)
                if msg.get_metadata("ontology") == "new_clustering":
                    self.agent.clusteringJID.append(sender)


    class RespondBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                sender = str(msg.sender).split('/')
                sender = sender[0]
                if msg.get_metadata("ontology") == "seek_classifier":
                    resp = Message(sender, "connection_agent@localhost", ' '.join(self.agent.classifierJID))
                    resp.set_metadata("performative", "response_connection")
                    resp.set_metadata("ontology", "classification")
                    await self.send(resp)
                if msg.get_metadata("ontology") == "seek_clustering":
                    resp = Message(sender, "connection_agent@localhost", ' '.join(self.agent.clusteringJID))
                    resp.set_metadata("performative", "response_connection")
                    resp.set_metadata("ontology", "clustering")
                    await self.send(resp)
    
    
    async def setup(self):
        self.classifierJID = list()
        self.clusteringJID = list()
        newConnection = Template()
        newConnection.set_metadata("performative", "new_connection")
        askTemplate = Template()
        askTemplate.set_metadata("performative", "ask")
        self.add_behaviour(self.NewConnection(), newConnection)
        self.add_behaviour(self.RespondBehaviour(), askTemplate)

if __name__ == "__main__":
    connection = ConnectionAgent("connection_agent@localhost", "connectionAgent")
    connection.start()
    connection.web.start("127.0.0.1", "10002")
