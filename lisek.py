#! /usr/bin/env python3
# Lisek Management App
# 0.0.4
# by kwojt(c)
#########################

from mail import IMAPObject
import pickle
import os
# from database import Table  # DEBUG ONLY
# Private settings and credentials
import mycred

# Setting up server objects
emailDown = IMAPObject(mycred.server, mycred.email, mycred.password)

# Parsing subscribers
if (os.path.isfile("subsEmail.sec")
        and not os.stat("subsEmail.sec").st_size == 0):
    subsEmailFile = open("subsEmail.sec", "rb")
    subsEmail = pickle.load(subsEmailFile)
    subsEmailFile.close()
    subsEmailNew = emailDown.parseNew("[EmailNewSubscriber]")
    subsEmail.mergeTable(subsEmailNew.table)
else:
    subsEmail = emailDown.parseAll("[EmailNewSubscriber]")
    subsEmail.renameColumn("[EmailNewSubscriber]", "email")

print("Email subscribers: ", len(subsEmail.table) - 1)
print(subsEmail.returnColumn("email"))
# testy = Table()
# testy.addColumn('email')
# testy.addRecord(['email', 'foo@bar.net'])
# testy.addRecord(['email', 'foo2@bar2.net'])
# print(testy.table)
# testyMail = emailDown.parseNew("[EmailNewSubscriber]")
# testyMail.renameColumn("[EmailNewSubscriber]", "email")
# testy.mergeTable(testyMail.table)
# print(testy.table)

# TODO Close files
