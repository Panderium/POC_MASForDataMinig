#!/usr/bin/python3
import time
from spade import container
from Agent.UserAgent import UserAgent
from Agent.ConnectionAgent import ConnectionAgent


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
