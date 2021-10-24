import sqlite3
from sqlite3 import Error
import functools

def sql_connection():
    """ sql_connection(): - подключение базы данных для чтения координат Ublox"""
    try:
        con = sqlite3.connect('server.db')
        print("База данных подключена")
        return con
    except Error:
        print("База данных не найдена")


#def bd_time_selector():


""" Ввод времени кадра, потом заменить на интерфейс"""
frame_year = 2021#input("Введи год кадра:  ")
frame_month = 9#input("Введи месяц кадра:  ")
frame_day = 6#input("Введи день кадра:  ")
frame_hour = 16#input("Введи час кадра:  ")
frame_minute = 13#input("Введи минуту кадра:  ")
frame_second = 19#input("Введи секунду кадра:  ")
frame_milisecond = 440*1000#int(input("Введи милисекунду кадра:  "))


"""Обозначаем вилку времён для получения нескольких ближайших точек из БД"""
milisecond_low = frame_milisecond - 200000
milisecond_hi = frame_milisecond + 200000
connect_sqlite3 = sql_connection()  #подключились к бд
cursor_sqlite3 = connect_sqlite3.cursor()   #создаём курсо


"""Запрашиваем в БД нужные координаты"""
cursor_sqlite3.execute('SELECT lat FROM locationsTABLE WHERE year == ? AND month == ? AND day == ? AND hour == ? AND minute = ? AND second = ? AND mS > ? AND mS < ?', (frame_year, frame_month, frame_day, frame_hour, frame_minute, frame_second, milisecond_low, milisecond_hi))
lats = cursor_sqlite3.fetchall()
cursor_sqlite3.execute('SELECT long FROM locationsTABLE WHERE year == ? AND month == ? AND day == ? AND hour == ? AND minute = ? AND second = ? AND mS > ? AND mS < ?', (frame_year, frame_month, frame_day, frame_hour, frame_minute, frame_second, milisecond_low, milisecond_hi))
lons = cursor_sqlite3.fetchall()
cursor_sqlite3.execute('SELECT mS FROM locationsTABLE WHERE year == ? AND month == ? AND day == ? AND hour == ? AND minute = ? AND second = ? AND mS > ? AND mS < ?', (frame_year, frame_month, frame_day, frame_hour, frame_minute, frame_second, milisecond_low, milisecond_hi))
mSs = cursor_sqlite3.fetchall()


""" Картежи в массивы"""
ms_Array = [0]*len(mSs)# массив размера для [хранения] нужных координат
ms_Array_norm = [0]*len(mSs)# массив размера для нормировки по времени кадра нужных координат
for i, score in enumerate(mSs):
    ms_Array[i] = functools.reduce(lambda sub, ele: sub * 10 + ele, (mSs[i]))

lat_Array = [0]*len(lats)# массив размера для выбора нужных координат
for i, score in enumerate(lats):
    lat_Array[i] = functools.reduce(lambda sub, ele: sub * 10 + ele, (lats[i]))

lon_Array = [0]*len(lons)# массив размера для выбора нужных координат
for i, score in enumerate(lons):
    lon_Array[i] = functools.reduce(lambda sub, ele: sub * 10 + ele, (lons[i]))

print(ms_Array)
#print(lat_Array)
#print(lon_Array)
"""Вычисляем 2 ближайших времени для усреднения координа по этим временам"""
#вычисляем модули разниц времён координат
for i, score in enumerate(ms_Array):
    ms_Array_norm[i] = abs(ms_Array[i]-frame_milisecond)
print(ms_Array_norm)
#находим минимальное значение = максимально блтзкое к времени кадра
t_min = 0.0
min_lat = 0.0
min_lon = 0.0
t_min_2 = 0.0
min_2_lat = 0.0
min_2_lon = 0.0
for i, score in enumerate(ms_Array_norm):
    if ms_Array_norm[i] > ms_Array_norm[i+1]:
        print("zerocode = ", ms_Array[i], ms_Array[i+1])
    else:
        t_min = ms_Array[i]# самый близкий элемент к нужному времени
        min_lat = lat_Array[i]
        min_lon = lon_Array[i]# минимальное нашли, теперь какое из соседних ближе к нужному времени
        if ms_Array_norm[i + 1] > ms_Array_norm[i - 1]:
            t_min_2 = ms_Array[i - 1]
            min_2_lat = lat_Array[i - 1]
            min_2_lon = lon_Array[i - 1]
            break
        else:
            t_min_2 = ms_Array[i + 1]
            min_2_lat = lat_Array[i + 1]
            min_2_lon = lon_Array[i +1]
            break
print("b = ", t_min, t_min_2)
""" Вычисляем усреднённую координату"""
lat_finish = min_lat + ((min_2_lat - min_lat) * ((frame_milisecond - t_min)/(t_min_2 - t_min)))#

print("lat_min    = ", min_lat)
print("lat_finish = ", lat_finish)
print("lat_max    = ", min_2_lat)