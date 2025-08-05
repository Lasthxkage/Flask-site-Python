from flask import Flask,render_template,url_for,request,redirect #request - Обращение к форме. Redirect - переадресация.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#render_template - функция, с помощью которой можно выводить определенный html-файл по вызову декоратора.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
class article(db.Model):
    #db.Model - наследование от объекта db.
    id = db.Column(db.Integer, primary_key = True)
    #.Column - создание ячейки. primary_key = True - ячейка будет уникальной.
    title = db.Column(db.String(50), nullable = False)
    intro = db.Column(db.String(100), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.now())
    #nullable = False - невозможность создать пустую статью
    def __repr__(self):
        return '<article %r>' % self.id
    # метод __repr__ нужен для получения объекта и его id из базы данных.
# файлом для работы фласка будет этот, т.к. мы передаем имя  в директиву __name__
@app.route('/main')
@app.route('/')
# у одного обработчика может быть несколько декораторов.
def main():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        Article = article(title=title,intro=intro,text=text)
        try:
            db.session.add(Article)
            db.session.commit()
            return redirect('/posts')
            #add - Добавление объекта, commit - сохранение.
        except:
            return 'Ошибка.'
    else:
        return render_template('create-article.html')
@app.route('/posts')
def posts():
    articles = article.query.order_by(article.date.desc()).all()
    #date.desc() - сортировка от более новых к новым старым.
    #article.query - обращение к базе данных по классу. .all/.first - вывод определенных данных из класса. .order_by - сортировка данных по полю
    return render_template('posts.html', articles=articles)
    #мы передаем в шаблон articles список articles.
@app.route('/posts/<int:id>')
def posts_detail(id):
    art = article.query.get(id)
    return render_template('post_detail.html', article=art)
@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    art = article.query.get_or_404(id)
    try:
        db.session.delete(art)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении статьи произошла ошибка.'
@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    art = article.query.get(id)
    if request.method == 'POST':
        art.title = request.form['title']
        art.intro = request.form['intro']
        art.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
            #add - Добавление объекта, commit - сохранение.
        except:
            return 'При редактировании статьи произошла ошибка.'
    else:
        return render_template('post_update.html', article=art)
    #get_or_404 - вывод данных, либо ошибка. подходит для работы с БД
    return render_template('post_detail.html', article=art)
# @app.route('/user/<string:name>/<int:id>')
# # <> - получение данных из url-адреса
# def user(name,id):
#     return 'User page: ' + name + ' ' + str(id)
# если мы запустим программу через этот файл, то он примет имя __main__.
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создает все таблицы, определенные в моделях
    app.run(debug=True)
# degub=True оставляет открытой консоль для багов. При окончании разработки, закрывается: =False