import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from imapclient import IMAPClient
from database import Table


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
        if isinstance(to, str):
            mail['To'] = to
        else:
            mail['Bcc'] = to
        mail['Subject'] = subject
        mail.attach(MIMEText(msg, 'html'))
        return mail.as_string()

    # Sends message
    def send_message(self, to, msg, from_=None):
        """
        Sends prepared MIME mail.

        Args:
        -----
        string: to -- target email address (can be list of many)
        string: msg -- prepared mail (can be converted with self.creates())
        string: from_ -- sender's email address (default self.login)

        Returns:
        --------
        Returns -1 in case of failure
        """
        if from_ is None:
            from_ = self.login
        if isinstance(to, str):
            to = [to]
        for address in to:
            try:
                self.smtpObj.sendmail(from_, address, msg)
            except smtplib.SMTPHeloError:
                print("HELLO error, ", address)
                return -1
            except smtplib.SMTPAuthenticationError:
                print("Auth error, ", address)
                return -1
            except smtplib.SMTPDataError:
                print("SMTP Data Error, ", address)
                return -1
            except smtplib.SMTPSenderRefused:
                print("Sender refused, ", address)
                return -1
            except smtplib.SMTPRecipientsRefused:
                print("Nobody get the mail, ", address)
                return -1
            except smtplib.SMTPException:
                print("Unknown SMTP Exception, ", address)
                return -1
            except:
                print("Unknown exception, ", address)
                return -1
            else:
                print("Succeed, ", address)

    def __del__(self):
        """
        Closes SMTP object.
        """
        self.smtpObj.quit()


class IMAPObject:
    """
    IMAPObject sets up connection  with IMAP server, download
    and sort mails, and download data from auto-mails from HTML forms
    to table.
    """
    def __init__(self, s_address, s_login, s_password):
        """
        Creates IMAPClient object, connects with server and try to
        log in.

        Args:
        -----
        string: s_address -- server address
        string: s_login -- login
        string: s_password -- password
        """
        try:
            self.server = IMAPClient(s_address, use_uid=True, ssl=False)
            self.server.login(s_login, s_password)
        except IMAPClient.Error:
            raise

    def parseAll(self, subject):
        """
        Parses all messages on the server.
        """
        select_info = self.server.select_folder("INBOX")
        print('%d messages in INBOX' % select_info[b'EXISTS'])

        messages = self.server.search([b'NOT', b'DELETED'])
        print("%d messages that aren't deleted" % len(messages))

        table = Table()
        table.addColumn(subject)
        response = self.server.fetch(messages, [b'ENVELOPE',
                                                b'FLAGS',
                                                b'BODY.PEEK[TEXT]'])
        encoded_subject = subject.encode()
        for msgid, data in response.items():
            if data[b'ENVELOPE'].subject == encoded_subject:
                value = data[b'BODY[TEXT]'][len(subject)+2:-2].decode()
                table.addRecord([subject, value])
        return table

    def parseNew(self, subject):
        """
        Parses new messages with given subject on the server
        """
        select_info = self.server.select_folder("INBOX")
        print('%d messages in INBOX' % select_info[b'EXISTS'])

        messages = self.server.search([b'NOT', b'SEEN'])
        print("%d messages that weren't seen" % len(messages))

        table = Table()
        table.addColumn(subject)
        response = self.server.fetch(messages, [b'ENVELOPE',
                                                b'FLAGS',
                                                b'BODY.PEEK[TEXT]'])
        encoded_subject = subject.encode()
        for msgid, data in response.items():
            if data[b'ENVELOPE'].subject == encoded_subject:
                value = data[b'BODY[TEXT]'][len(subject)+2:-2].decode()
                table.addRecord([subject, value])
        return table

# TODO:
# - Update docstring
