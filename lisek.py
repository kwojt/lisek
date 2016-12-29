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
system.setupIMAP(mycred.server, mycred.email, mycred.password)
system.setupSMTP(mycred.server, mycred.server_port,
                 mycred.email, mycred.password)
system.parseBase()

print("System ready.\n")

while True:
    print("Please select one option:")
    print("=========================")
    print("1. Broadcast an email to all subscribers")
    print("2. Download phone numbers to file")
    print("0. Exit")
    print("Well, that's it for now. Choose.")
    cin = -1
    while cin != 2 and cin != 1 and cin != 0:
        cin = int(input())
        if cin == 1:
            system.broadcastMail()
        elif cin == 2:
            system.phoneNumbersToFile()
    if cin == 0:
        break
