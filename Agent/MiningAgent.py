#!/usr/bin/python3
import time
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.template import Template
from spade.message import Message

import numpy as np
from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

class MiningAgent(Agent):
    class NotifierBehaviour(OneShotBehaviour):
        async def run(self):
            message = Message("connection_agent@localhost", None)
            message.set_metadata("performative", "new_connection")
            message.set_metadata("ontology", "new_classifier")
            await self.send(message)

    class ClassificationBehaviour(CyclicBehaviour):

        async def run(self):
            msg = await self.receive()
            if msg:
                if msg.get_metadata("ontology") == "classification":
                    print("Mining task")
                    iris = datasets.load_iris()
                    iris_X = iris.data
                    iris_y = iris.target
                    np.random.seed(0)
                    indices = np.random.permutation(len(iris_X))
                    iris_X_train = iris_X[indices[:-10]]
                    iris_y_train = iris_y[indices[:-10]]
                    iris_X_test = iris_X[indices[-10:]]
                    iris_y_test = iris_y[indices[-10:]]
                    knn = KNeighborsClassifier()
                    knn.fit(iris_X_train, iris_y_train) 
                    accuracy = accuracy_score(iris_y_test, knn.predict(iris_X_test))
                    sender = str(msg.sender).split("/")[0]
                    body = str(accuracy) + " KNeighbors"
                    message = Message(sender, "class_agent@localhost", body)
                    message.set_metadata("performative", "classification_result")
                    await self.send(message)



    async def setup(self):
        classifierTemplate = Template()
        classifierTemplate.set_metadata("performative", "predict")
        self.add_behaviour(self.ClassificationBehaviour(), classifierTemplate)
        self.add_behaviour(self.NotifierBehaviour())
    
if __name__ == "__main__":
    mining = MiningAgent("class_agent@localhost", "classAgent")
    mining.start()
    mining.web.start("127.0.0.1", "10001")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break