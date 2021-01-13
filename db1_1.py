# Импорт библиотеки
import sqlite3
name_of_database = input()
# Подключение к БД
con = sqlite3.connect(name_of_database)

# Создание курсора
cur = con.cursor()

# Выполнение запроса и получение всех результатов
result = cur.execute("""SELECT title FROM films
  WHERE year > 1996 and genre in
(SELECT id FROM genres 
    WHERE title = 'музыка' or title = 'анимация')""").fetchall()

# Вывод результатов на экран
for elem in result:
    print(elem[0])

con.close()