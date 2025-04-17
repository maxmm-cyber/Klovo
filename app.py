from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import*
from sql_scripts import*
from random import*
import sqlite3


DB = 'blog.db'
app = Flask(__name__)  # Створюємо веб–додаток Flask

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


    
@app.route("/")  # Вказуємо url-адресу для виклику функції
def index():
    #articles = get_all_articles()
    

    return render_template("index.html")

@app.route("/polityka")
def polityka():
    return render_template("polityka.html")

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/menu")  # Вказуємо url-адресу для виклику функції
def menu():
    articles = get_all_articles()  # Отримуємо всі статті з бази даних
    
    return render_template("menu.html", articles=articles)  # Передаємо articles в шаблон 

@app.route('/comms', methods=['GET', 'POST'])
def comms():
    if request.method == 'POST':
        nickname = request.form['nickname']
        comment = request.form['comment']

        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO comments (author, text) VALUES (?, ?)", (nickname, comment))

                         

        return redirect('/')

    with sqlite3.connect(DB) as conn:
        comments = conn.execute("SELECT * FROM comments ORDER BY created DESC").fetchall()


    return render_template('comms.html', comments=comments)

@app.route('/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    return redirect('/')
   


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # автоматичне оновлення шаблонів
    app.run(debug=True)  # Запускаємо веб-сервер з цього файлу в режимі налагоджея