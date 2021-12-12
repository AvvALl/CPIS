from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from client.utils import getDateForPreview
import ntpath

class Message:
    def __init__(self):
        self.opened=False
        pass

    def path_leaf(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)


    """
    generates a message to send
    parameters:
    sender_email: email which send message
    receiver_email: list or string of receiver email
    body: string body message
    mailing: flag of mailing state
    attachments: all names of attachment files
    
    """
    def buildMessage(self, sender_email, receiver_email, subject, body, attachments=[], mailing=False, type_message=True):
        self.message = MIMEMultipart()
        self.message["From"]=sender_email
        self.message["Subject"]=subject
        if mailing:
            self.message["Bcc"]=receiver_email
        else:
            self.message["To"] = receiver_email[0]
        if type_message:
            self.message.attach(MIMEText(body, "plain"))
        else:
            self.message.attach(MIMEText(body, "html"))

        if len(attachments)!= 0:
            for file in attachments:
                part=MIMEBase("application", "octet-stream")
                part.set_payload(file[1])
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {file[0]}",)
                self.message.attach(part)

        return self.message

    def readMessage(self,uid, msg):
        self.uid=uid
        self.fromAddr=msg["From"]  if msg["From"] is not None else ' '
        self.toAddr=msg["To"] if msg["To"] is not None else ' '
        self.subject=msg["Subject"] if msg["Subject"] is not None else ' '
        self.date=getDateForPreview(msg["Date"])
        self.body = ""
        self.attachments=[]
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    self.body+=part.get_payload(decode=True).decode('utf-8')
                elif part.get('Content-Disposition') is not None:
                    self.attachments.append((part.get_filename(), part.get_payload(decode=True)))
                    pass
        else:
            if msg.get_content_type() == "text/plain" or msg.get_content_type()=="text/html":
                self.body += msg.get_payload(decode=True).decode('utf-8')
        return self

    def readMessage2(self, uid, msg):
        self.uid, self.id=uid,msg.get("Message-ID")
        self.fromAddr = msg["From"] if msg["From"] is not None else ' '
        self.toAddr = msg["To"] if msg["To"] is not None else ' '
        self.subject = msg["Subject"] if msg["Subject"] is not None else ' '
        self.date = getDateForPreview(msg["Date"])
        self.body = ""
        self.attachments = []
        return self
    def getFilenamesAttach(self):
        return [filename[0] for filename in self.attachments]


