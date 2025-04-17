import sqlite3


def get_all_articles():
    conn = sqlite3.connect("blog.db")  # Підключаємося до бази даних
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")  # Отримуємо всі записи з таблиці menu
    articles = cursor.fetchall()  # Забираємо всі записи в список
    conn.close()  # Закриваємо з'єднання
    return articles