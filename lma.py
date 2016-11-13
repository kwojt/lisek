#! /usr/bin/env python3
# Lovehard Management App
# 0.0.4
# by kwojt(c)
#########################

from imapclient import IMAPClient
# Private settings and credentials
import mycred

# Getting mail from the server
mailGet = IMAPClient(mycred.server, use_uid=True, ssl=False)
mailGet.login(mycred.email, mycred.password)

select_info = mailGet.select_folder("INBOX")
print('%d messages in INBOX' % select_info[b'EXISTS'])

messages = mailGet.search([b'NOT', b'DELETED'])
print("%d messages that aren't deleted" % len(messages))

print()
print("Messages:")
response = mailGet.fetch(messages, [b'FLAGS', b'RFC822.SIZE'])
for msgid, data in response.items():
    print('   ID %d: %d bytes, flags=%s' % (msgid,
                                            data[b'RFC822.SIZE'],
                                            data[b'FLAGS']))
