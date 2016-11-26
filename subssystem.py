from mail import IMAPObject, SMTPObject
import pickle
# import os


class subsSystem:
    """
    Subscription management system.
    """

    def setupSMTP(self, server, login, password):
        self.emailDown = IMAPObject(server, login, password)
        pass

    def setupIMAP(self, server, port, login, password):
        self.emailUp = SMTPObject(server, port, login, password)

    def parseBase(self, subject, keyName):
        # if (os.path.isfile(keyName+".sec")
        #         and not os.stat(keyName+".sec").st_size == 0):
        #     subsBaseFile = open(keyName+".sec", "rb")
        #     self.subsBase = pickle.load(subsBaseFile)
        #     subsBaseFile.close()
        #     subsBaseNew = self.emailDown.parseNew(subject)
        #     subsBaseNew.renameColumn(subject, keyName)
        #     self.subsBase.mergeTable(subsBaseNew.table)
        # else:
        self.subsBase = self.emailDown.parseAll(subject)
        self.subsBase.renameColumn(subject, keyName)
        subsBaseFile = open(keyName+".sec", "wb")
        pickle.dump(self.subsBase, subsBaseFile,
                    pickle.HIGHEST_PROTOCOL)
        subsBaseFile.close()
        print("Subscribers: ", len(self.subsBase.table) - 1)

    def broadcastMail(self):
        cin = input("Do you want to broadcast message from file (y/n): ")
        if cin == "y" or cin == "yes":
            dir = input("File name: \n")
            msgFile = open(dir, "r")
            msgContent = msgFile.read()
            print(msgContent)
            msgFile.close()
            subject = input("Email subject?\n")
            # Check if email was not send earlier
            self.subsBase.addColumn(dir)
            users = self.subsBase.returnColumn("email")
            print(users)
        print("-----------------------------------------------------")
        for user in users:
            msg = self.emailUp.create_message(user, msgContent, subject)
            if self.emailUp.send_message(user, msg) != -1:
                self.subsBase.modifyRecord(["email", user], [dir, True])
