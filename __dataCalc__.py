import sqlite3
from sqlite3 import Error
#cursorObj = 0
def sql_connection():# подключаемся к серверу бд

    try:
        con = sqlite3.connect('server.db')
        return con
    except Error:
        print(Error)
def sql_table(con): # Проверяем наличие бд с табличкой и создаём, если нет такой

    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS locationsTABLE (year integer, month integer, day integer, hour integer, minute integer, second integer, mS real, lat real, long real, speed integer)")
    con.commit()
def sql_insert(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO locationsTABLE (year, month, day, hour, minute, second, mS, lat, long, speed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', entities)
    con.commit()

con = sql_connection()
cursorObj = con.cursor()
sql_table(con)
reqwest = (2021, 9, 6, 10, 33, 25.5, 682)
sql_select_query = 'SELECT * FROM locationsTABLE WHERE YEAR = ' + str(reqwest[0]) + ' AND MONTH =' + str(reqwest[1]) + ' AND DAY = '+ str(reqwest[2]) +' AND HOUR = '+ str(reqwest[3]) +' AND MINUTE = '+ str(reqwest[4])# +' AND SECOND = '+ str(reqwest[5])
result = cursorObj.execute(sql_select_query).fetchall()
#print(result)
cursorObj.close()
for x in result:
    #for y in x:
    print(x)
print(result[0][4])
print(reqwest[5])
fined = 0
i = 3-2-1
while fined == 0:
    if result[i][5] < reqwest[5] and result[i+1][5] > reqwest[5]:
        fined = 1
        GPS_L = result[i]
        GPS_H = result[i+1]
    else:
        i+=1
print(GPS_L)
print(GPS_H)
GPS_Coefitient = (GPS_H[6] - GPS_L[6])/(reqwest[6] - GPS_L[6])
print(GPS_Coefitien)