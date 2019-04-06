#!/usr/bin/python3
from spade.message import Message

def parseRequest( request):
    request = request.split()
    if (request[0] == "classification" or request[0] == "clustering" or request[0] == "association") and len(request) > 1:
        return request
    return 1

def formMessage(sender, to, performative, ontology, other=None):
    message = Message()
    message.sender = sender
    message.to = to
    message.set_metadata("performative", performative)
    message.set_metadata("ontology", ontology)
    if other:
        for value in other.items():
            message.set_metadata(value[0], value[1])

    return message

