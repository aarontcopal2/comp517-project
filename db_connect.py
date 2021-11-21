import pyodbc 

databaseName = 'master'
username = 'comp517-1'
password = 'abcd'
server = 'tcp:168.5.62.67;PORT=1433'
driver= '{SQL Server}'
CONNECTION_STRING = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+databaseName+';UID='+username+';PWD='+ password


conn = pyodbc.connect(CONNECTION_STRING)

cursor = conn.cursor()
cursor.execute('SELECT * FROM features')

for i in cursor:
    print(i)