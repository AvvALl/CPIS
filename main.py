from client.messages import  Message

from client.imapClient import imap
from client.smtpClient import smtp
login, passw='avvallls@yandex.ru','13052000zx'

sm=smtp()
im=imap()

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

print(body)