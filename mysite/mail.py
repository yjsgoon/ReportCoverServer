import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COVER_FOLDER = '/home/reportcover/mysite/cover/'

fromaddr = 'reportcoversender@gmail.com'
toaddr = 'yjsgoon@gmail.com'

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Univ Cover'

body = 'Have a nice day!~'

msg.attach(MIMEText(body, 'plain'))

filename = "dankook.pdf"
attachment = open(COVER_FOLDER + filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, 'dbswltn213')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()