import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPObject:
    """
    SMTPObject serves for connecting to SMTP server
    and sending mails.
    """

    def __init__(self, server, port, login, password):
        """
        Initializes SMTP object
        and connects with the SMTP server,
        also tries to log in.

        Args:
        -----
        string: server -- SMTP server address to connect to.
        int: port -- server's port
        string: login -- just login
        string: password -- password for login

        Returns:
        --------
        Function returns -1 if exception occured.
        """
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        try:
            self.smtpObj = smtplib.SMTP(server, port)
            self.smtpObj.starttls()
            self.smtpObj.login(login, password)
        except smtplib.SMTPHeloError:
            print("HELO error")
            return -1
        except smtplib.SMTPAuthenticationError:
            print("Auth error")
            return -1
        except smtplib.SMTPException:
            print("Unknown SMTP error")
            return -1
        except:
            print("Unknown exception")
            return -1

    # Prepare message
    def create_message(self, to, msg, subject="Unknown subject", from_=None):
        """
        Creates message MIME object.

        Args:
        -----
        string: to -- target's email
        string: msg -- just message body
        string: subject -- subject of a mail (defaut "Unknown subject")
        string: from_ -- sender email adress (default self.login)

        Returns:
        --------
        string: _mail.as_string() -- prepared to be send with SMTP.sendmail()
        """
        if from_ is None:
            from_ = self.login
        mail = MIMEMultipart()
        mail['From'] = from_
        mail['To'] = to
        mail['Subject'] = subject
        mail.attach(MIMEText(msg, 'plain'))
        return mail.as_string()

    # Sends message
    def send_message(self, to, msg, from_=None):
        """
        Sends prepared MIME mail.

        Args:
        -----
        string: to -- target email address
        string: msg -- prepared mail (can be converted with self.creates())
        string: from_ -- sender's email address (default self.login)

        Returns:
        --------
        Returns -1 in case of failure
        """
        if from_ is None:
            from_ = self.login
        try:
            self.smtpObj.sendmail(from_, to, msg)
        except smtplib.SMTPHeloError:
            print("HELLO error")
            return -1
        except smtplib.SMTPAuthenticationError:
            print("Auth error")
            return -1
        except smtplib.SMTPDataError:
            print("SMTP Data Error")
            return -1
        except smtplib.SMTPSenderRefused:
            print("Sender refused")
            return -1
        except smtplib.SMTPRecipientsRefused:
            print("Nobody get the mail")
            return -1
        except smtplib.SMTPException:
            print("Unknown SMTP Exception")
            return -1
        except:
            print("Unknown exception")
            return -1
        else:
            print("Succeed")

    def __del__(self):
        """
        Closes SMTP object.
        """
        self.smtpObj.quit()
