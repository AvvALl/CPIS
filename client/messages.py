from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ntpath

class Message:
    def __init__(self):
        pass

    def path_leaf(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def getDateForPreview(self,date):
        correctDate = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        return correctDate.strftime("%H-%M-%d-%b-%Y").split('-')

    """
    generates a message to send
    parameters:
    sender_email: email which send message
    receiver_email: list or string of receiver email
    body: string body message
    mailing: flag of mailing state
    attachments: all names of attachment files
    
    """
    def buildMessage(self, sender_email, receiver_email, subject, body, attachments=None, mailing=False, type_message=True):
        self.message = MIMEMultipart()
        self.message["From"]=sender_email
        self.message["Subject"]=subject
        if mailing:
            self.message["Bcc"]=receiver_email
        else:
            self.message["To"] = receiver_email
        if type_message:
            self.message.attach(MIMEText(body, "plain"))
        else:
            self.message.attach(MIMEText(body, "html"))

        if attachments is not None:
            for filename in attachments:
                with open(filename, "rb")  as file:
                    part=MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                base_filename=self.path_leaf(filename)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {base_filename}",)
                self.message.attach(part)

        return self.message

    def readMessage(self, msg):
        self.fromAddr=msg["From"]
        self.toAddr=msg["To"]
        self.subject=msg["Subject"]
        self.date=self.getDateForPreview(msg["Date"])
        self.body = ""
        self.attachments=[]
        if msg.is_multipart():
            tmp=""
            for part in msg.walk():
                if part.get_content_type()=="text/plain":
                    self.body+=part.get_payload(decode=True).decode('utf-8')
                elif part.get('Content-Disposition') is not None:
                    self.attachments.append((part.get_filename(), part.get_payload(decode=True)))
        else:
            if msg.get_content_type() == "text/plain":
                self.body += msg.get_payload(decode=True).decode('utf-8')
        return self
    def getFilenamesAttach(self):
        return [filename[0] for filename in self.attachments]


