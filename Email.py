from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import Config
import ExceptionManager
import datetime

exceptionFileName = "Email.py"

class Email:
    def __init__(self, toaddr):
        self.fromaddr = Config.getMailFrom()
        if toaddr == None:
            self.toaddr = Config.getMailTo()
        else:
            self.toaddr = toaddr
        self.password = Config.getMailPassword()

        self.msg = MIMEMultipart()

    def attach(self, file):
        try:
            part = MIMEBase('application', 'octet-stream')
            
            filename = file.name
            attachment = open(file.spoolPath, "rb")
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            "attachment; filename= %s" % filename)
            self.msg.attach(part)
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "attach", exceptionFileName)

    def sendmail(self, branch):
        dateTime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.msg['From'] = self.fromaddr
        self.msg['To'] = self.toaddr
        self.msg['Subject'] = "Ziraat " + branch + " Deploy - " + dateTime
               
        self.body = "Ziraat " + branch + " Deployu Tamamlanmıştır. \n Çalışan scriptlerin sonuçları ek olarak eklendi."

        self.msg.attach(MIMEText(self.body, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.fromaddr, self.password)
            text = self.msg.as_string()
            server.sendmail(self.fromaddr, self.toaddr, text)
            server.quit()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "sendmail", exceptionFileName)
            return False
        return True