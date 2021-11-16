import pyodbc 

databaseName = 'hw1'
username = 'comp517'
password = 'comp517'
server = 'DESKTOP-J68AUP8'
driver= '{SQL Server Native Client 11.0}'
CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password


conn = pyodbc.connect(CONNECTION_STRING)

cursor = conn.cursor()
cursor.execute('SELECT * FROM features')

for i in cursor:
    print(i)