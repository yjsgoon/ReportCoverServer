from pushjack import GCMClient

client = GCMClient(api_key='AIzaSyCcFYoLmotIiI9M1l_oTyp8xdVr4lL-y_I')

msg = 'hello'
print (msg)
ids = 'ef-NwOq3VjU:APA91bHd22Tp1DqMP9cq6jb6O7hCpCkDPEeFRpYGHhQ9DC8s_aIlihsf_XYN4oDZYSTYL9Ce3NI8-nHiQAv5rV_EuHBuaiolthXrbbwNEj6XcsvxEnVNcrnN87gZxpfTllzaxV72HkCZ'
message = {"title":"Report Cover", "message":msg, "count":34}
client.send(ids, message);