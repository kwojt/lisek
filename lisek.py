#! /usr/bin/env python3
# Lisek Management App
# 0.0.4
# by kwojt(c)
#########################

# from database import Table  # DEBUG ONLY
# Private settings and credentials
import mycred
from subssystem import subsSystem

print("Setting up.")

system = subsSystem()
system.setupSMTP(mycred.server, mycred.email, mycred.password)
system.setupIMAP(mycred.server, mycred.server_port,
                 mycred.email, mycred.password)

system.parseBase("[EmailTest]", "email")

system.broadcastMail()

# while True:
#     print("Please select one option:")
#     print("1. Broadcast an email to all subscribers")
#     print("0. Exit")
#     cin = -1
#     while cin != 1 and cin != 0:
#         cin = input()
#         if cin == 1:
#             # subsSystem.broadcast()
#             pass
#         elif cin == 0:
#             break


# TODO Close files
