
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, send_file
from pushjack import GCMClient
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import MySQLdb
import json
import smtplib

LOGO_FOLDER = '/home/reportcover/mysite/image_logo/'
COVER_FOLDER = '/home/reportcover/mysite/cover/'

app = Flask(__name__)

conn = MySQLdb.connect('reportcover.mysql.pythonanywhere-services.com',
                       'reportcover', 'dbswltn213', 'reportcover$reportcover')
cursor = conn.cursor()

@app.route('/')
def hello_world():
    return 'Hello from ReportCover!'

@app.route('/loadUniv', methods = ['GET'])
def loadUniv():
    cursor.execute('select * from univ_information')
    result = []

    columns = tuple( [d[0] for d in cursor.description] )

    for row in cursor:
        result.append(dict(zip(columns, row)))

    return json.dumps(result)

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    email = request.form['email']
    gcmId = request.form['gcmId']

    query = "insert ignore into account (Email, GcmId) values ('" + email + "', '" + gcmId + "');"

    cursor.execute(query)
    conn.commit()

    return 'ok'

@app.route('/selectUniv', methods = ['POST'])
def selectUniv():
    if request.method == 'POST':
        toaddr = request.form['email']
        univNumber = request.form['univNumber']

        fromaddr = 'reportcoversender@gmail.com'

        gcmId = []
        query = "select GcmId from account where Email='" + toaddr + "';"
        cursor.execute(query)

        gcmId = str(cursor.fetchone()[0])

        fileName = []
        query = "select FileName from univ_information where UnivNumber='" + univNumber + "';"
        cursor.execute(query)

        fileName = str(cursor.fetchone()[0])

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Univ Cover'

        body = 'Have a nice day!~'

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(COVER_FOLDER+fileName, "rb")

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

        message = {"title":"ReportCover", "message":gcmMsg, "count":34}
        client.send(gcmId, message);

        return 'ok'

    return 'error'

@app.route('/image/<fileName>', methods=['GET'])
def loadImage(fileName):
    if request.method == 'GET':
	    return send_file(LOGO_FOLDER+fileName, mimetype='image')

