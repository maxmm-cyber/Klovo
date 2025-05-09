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
    

    return render_template("index.html")

@app.route("/polityka")
def polityka():
    return render_template("polityka.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/alert")
def alert():
    return render_template("alert.html")
@app.route("/search")
def search():
    query = request.args.get('query',"")
    articles = search_articles(query)
    return render_template("search.html",articles=articles)



@app.route("/menu")  
def menu():
    articles = get_all_articles()  
    
    return render_template("menu.html", articles=articles)  

@app.route('/comms', methods=['GET', 'POST'])
def comms():
    if request.method == 'POST':
        nickname = request.form['nickname']
        comment = request.form['comment']

        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO comments (author, text) VALUES (?, ?)", (nickname, comment))
            conn.commit()

                         

        return redirect('/')

    with sqlite3.connect(DB) as conn:
        comments = conn.execute("SELECT * FROM comments ORDER BY created DESC").fetchall()
        conn.commit()


    return render_template('comms.html', comments=comments)


def insert_order(name, address):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (name, address) VALUES (?, ?)", (name, address))
        conn.commit()

def get_all_orders():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, address FROM orders")
        return cursor.fetchall()

@app.route('/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    return redirect('/')
   

@app.route("/article/<int:menu_id>")
def article_page(menu_id):  
    article = get_article(menu_id)
    return render_template("article_page.html", article=article)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    address = request.form.get('address')
    insert_order(name, address)
    return redirect('/orders')

@app.route('/orders')
def orders():
    all_orders = get_all_orders()
    return render_template('orders.html', orders=all_orders)






if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True 
    app.run(debug=True)  