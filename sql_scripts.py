import sqlite3


def get_all_articles():
    conn = sqlite3.connect("blog.db") 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu") 
    articles = cursor.fetchall() 
    conn.close()  
    return articles

def get_article(menu_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu WHERE id=?", [menu_id])
    article = cursor.fetchone() 
    conn.close()
    return article

def search_articles(search_query):
    conn = sqlite3.connect("blog.db") 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM menu WHERE title LIKE ?",['%'+search_query+'%']) 
    articles = cursor.fetchall() 
    conn.close()  
    return articles
