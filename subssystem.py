from mail import IMAPObject, SMTPObject
import pickle
import os


class subsSystem:
    """
    Subscription management system.
    """

    def setupSMTP(self, server, login, password):
        self.emailDown = IMAPObject(server, login, password)
        pass

    def setupIMAP(self, server, port, login, password):
        self.emailUp = SMTPObject(server, port, login, password)

    def parseBase(self):
        if (os.path.isfile("subsEmail.sec")
                and not os.stat("subsEmail.sec").st_size == 0):
            subsEmailFile = open("subsEmail.sec", "rb")
            self.subsEmail = pickle.load(subsEmailFile)
            subsEmailFile.close()
            subsEmailNew = self.emailDown.parseNew("[EmailTest]")
            subsEmailNew.renameColumn("[EmailTest]", "email")
            self.subsEmail.mergeTable(subsEmailNew.table)
        else:
            self.subsEmail = self.emailDown.parseAll("[EmailTest]")
            self.subsEmail.renameColumn("[EmailTest]", "email")
            subsEmailFile = open("subEmail.sec", "wb")
            pickle.dump(self.subsEmail, subsEmailFile,
                        pickle.HIGHEST_PROTOCOL)
            subsEmailFile.close()
        print("Email subscribers: ", len(self.subsEmail.table) - 1)

    def broadcastMail(self):
        cin = input("Do you want to broadcast message from file (y/n): ")
        if cin == "y" or cin == "yes":
            cin = input("File directory: \n")
            msgFile = open(cin, "r")
            msgContent = msgFile.read()
            print(msgContent)
            msgFile.close()
            # Check if email was not send earlier
            subsEmail.addColumn(cin)
            users = subsEmail.returnColumn("email")
            print(users)
        print("-----------------------------------------------------")
        for user in users:
            msg = emailUp.create_message(user, msgContent, "#TEST")
            if emailUp.send_message(user, msg) != -1:
                subsEmail.modifyRecord(["email", user], [cin, True])
