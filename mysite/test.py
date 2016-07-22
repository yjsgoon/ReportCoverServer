from pushjack import GCMClient
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import MySQLdb
import smtplib

conn = MySQLdb.connect('reportcover.mysql.pythonanywhere-services.com',
                       'reportcover', 'dbswltn213', 'reportcover$reportcover')
cursor = conn.cursor()

COVER_FOLDER = '/home/reportcover/mysite/cover/'

toaddr = 'yjsgoon@gmail.com'
univNumber = '11'

fromaddr = 'reportcoversender@gmail.com'

gcmId = []
query = "select GcmId from account where Email='" + toaddr + "';"
cursor.execute(query)

for row in cursor:
    gcmId = row

fileName = []
query = "select FileName from univ_information where UnivNumber='" + univNumber + "';"
cursor.execute(query)

fileName = str(cursor.fetchone()[0])

coverFolder = COVER_FOLDER + str(fileName)

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Univ Cover'

body = 'Have a nice day!~'

msg.attach(MIMEText(body, 'plain'))

attachment = open(coverFolder, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % fileName)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, 'dbswltn213')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()

client = GCMClient(api_key='AIzaSyCcFYoLmotIiI9M1l_oTyp8xdVr4lL-y_I')
gcmMsg = "cover transmission complete"

print (msg)
message = {"title":"ReportCover", "message":gcmMsg, "count":34}
client.send(gcmId, message);