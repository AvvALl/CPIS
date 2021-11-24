from client.messages import  Message

from client.imapClient import imap
from client.smtpClient import smtp
from client.client import client
from encryption.crypt import  crypt
login, passw, email='avvallls','13052000zx','yandex'
"""
sm=smtp(email)
im=imap(email)

sm.login(login,passw)
im.login(login, passw)
print(im.getFolders())

lst=im.getMessagesFromFloder("INBOX")
if lst[0].is_multipart():
    str = ""
    for payload in lst[0].get_payload():
        if payload.get('Content-Disposition'):
            continue

        body = payload.get_payload(decode=True).decode('utf-8')
        str += body
    body=str
"""
"""
cl=client(login, passw, email)
cl.loginToAccaunt()
print(cl.server_imap.getFolders())
"""
lst=["sas", "kas"]
frt=dict.fromkeys(lst, [])
print(frt)
