"""   прошивка для меги GPS__x_y_v_I2C_MEGA

    mega/ESP32  ->  f9p
    провода между платами
          SCL   ->  J8.10
          SDA   ->  J8.9

"""
import serial, time
import sqlite3
from sqlite3 import Error

ser = serial.Serial("COM8")
ser.baudrate = 1000000

def sql_connection():
    """ sql_connection(): - подключение базы данных для записи координат Ublox"""
    try:
        con = sqlite3.connect('server.db')
        return con
    except Error:
        print(Error)

def sql_table(con):
    """ sql_table(con): - создание таблицы в БД"""
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS locationsTABLE (year integer, month integer, day integer, hour integer, minute integer, second integer, mS integer, lat real, long real)")
    con.commit()

def sql_insert(con, entities):
    """ sql_insert(con, entities): - запись данных в БД"""
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO locationsTABLE( year, month, day, hour, minute, second, mS, lat, long) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', entities)
    con.commit()

def time_micros (f):
    """ time_micros (f): - микросекунды времен на рабочей станции"""
    f = f%1*1000000 # отбрасываем целую часть, дробная = количество микросекунд
    return ((f * 10**0) // 1) / 10**0 # 10**x - (x) = количество знаков после запятой? тут х = 0

def COM_reed_digits(lenght_of_range): #читаем координаты из порта соответствующей длины
    """ COM_reed_digits(lenght_of_range): - чтение данных из порта длинной lenght_of_range"""
    line = bytearray(b'')
    x = 0.0
    for i in range(lenght_of_range-1):
        line = ser.read()
        #print(line)
        x = x + (int.from_bytes(line, "big") - 48)*10**(lenght_of_range-1-i)
        #print(x)
    return x

def get_GPS_from_Serial(): #забрать данные из порта
    """ get_GPS_from_Serial(): - возвращает готовые координаты от comPort """
    lon = 0.0
    lat = 0.0
    speed = 0
    if  ser.read() == (b'L'):
        if ser.read() == (b'K'):
            if ser.read() == (b'J'):
                lat = COM_reed_digits(12)
                lat/=10000000000
                #print("LAT = ", lat)
                lon = COM_reed_digits(12)
                lon/=10000000000
                #print("LON = ", lon)
                #speed = (10000000 - COM_reed_digits(7))/10
                #print("SPD = ", speed)
    return (lat, lon)

con = sql_connection()
sql_table(con)
entities = (2021, 9, 2, 23, 54, 33, 555, 92.567961456354325, 55.994756347653247, 995599)
#sql_insert(con, entities)

while True :
    gps = get_GPS_from_Serial()
    t = time.localtime()
    x = time.time()
    entities = (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, time_micros(x), gps[0], gps[1])
    print(entities)
    sql_insert(con, entities)