#! /usr/bin/env python3
# Lisek Management App
# 0.0.4
# by kwojt(c)
#########################

from mail import IMAPObject, SMTPObject
import pickle
import os
# from database import Table  # DEBUG ONLY
# Private settings and credentials
import mycred

# Setting up server objects
emailDown = IMAPObject(mycred.server, mycred.email, mycred.password)
emailUp = SMTPObject(mycred.server, mycred.server_port,
                     mycred.email, mycred.password)

# Parsing subscribers
if (os.path.isfile("subsEmail.sec")
        and not os.stat("subsEmail.sec").st_size == 0):
    subsEmailFile = open("subsEmail.sec", "rb")
    subsEmail = pickle.load(subsEmailFile)
    subsEmailFile.close()
    subsEmailNew = emailDown.parseNew("[EmailTest]")
    subsEmailNew.renameColumn("[EmailTest]", "email")
    subsEmail.mergeTable(subsEmailNew.table)
else:
    subsEmail = emailDown.parseAll("[EmailTest]")
    subsEmail.renameColumn("[EmailTest]", "email")

print("Email subscribers: ", len(subsEmail.table) - 1)

# Sending message from certain file
cin = input("Do you want to broadcast message from file (y/n): ")
if cin == "y" or cin == "yes":
    cin = input("File directory: \n")
    msgFile = open(cin, "r")
    subsEmail.addColumn(cin)
    print(msgFile.read())
    users = subsEmail.returnColumn("email")
    print(users)
    print("-----------------------------------------------------")
    for user in users:
        msg = emailUp.create_message(user, msgFile.read(), "#TEST")
        if not emailUp.send_message(user, msg):
            subsEmail.modifyRecord(["email", user], [cin, True])

print(subsEmail.table)


# TODO Close files
