# Lovehard Managing App
# 0.0.1
# by kwojt

import smtplib

fromaddr = "kadotwojt@gmail.com"
toaddr = "kwojt@g.pl"

msg = "Something something!"

# Credidentials
# removed because of security reasons...
# just add username and password here, ex
# username = "sth@gmail.com"
# password = "iamlame"
import credentials

# Sending mail
server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username, password)
server.sendmail(fromaddr, toaddr, msg)
server.quit()
