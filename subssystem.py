from mail import IMAPObject, SMTPObject


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
        self.subsEmail = self.emailDown.parseAll("[EmailNewSubscriber]")
        self.subsEmail.renameColumn("[EmailNewSubscriber]", "email")
        self.subsSMS = self.emailDown.parseAll("[SMSNewSubscriber]")
        self.subsSMS.renameColumn("[SMSNewSubscriber]", "sms")
        print("SMS subscribers: ", len(self.subsSMS.table)-1)
        print("Email subscribers: ", len(self.subsEmail.table)-1)

    def broadcastMail(self):
        cin = input("Do you want to broadcast message from file (y/n): ")
        if cin == "y" or cin == "yes":
            dir = input("File name: \n")
            msgFile = open(dir, "r")
            msgContent = msgFile.read()
            print(msgContent)
            msgFile.close()
            subject = input("Email subject?\n")
            users = self.subsEmail.returnColumn("email")

        print("\nSending mail to all users")
        print("-----------------------------------------------------")
        for user in users:
            msg = self.emailUp.create_message(user, msgContent, subject)
            self.emailUp.send_message(user, msg)
        print("Done \n")

    def phoneNumbersToFile(self):
        print("Saving users to SendSMSHere.sec")
        divide = int(input("How many numbers in group?\n"))
        writeFile = open("SendSMSHere.sec", "w")

        iteruser = iter(self.subsSMS.table)
        next(iteruser)
        for i, user in enumerate(iteruser, 1):
            writeFile.write(user['sms']+",\n")
            if divide != 0 and (i % divide) == 0:
                writeFile.write("-----------------------------------\n")

        print("Users saved.\n")
