from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float
from sqlalchemy.exc import IntegrityError
from flask import flash

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)   

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SECRET_KEY"] = '12345678'
db.init_app(app)

#------------------------------- DATABASE MODEL ---------------------------#
class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str] = mapped_column(unique=False)
    rating: Mapped[float] = mapped_column(unique=False)
 
#------------------------------- CREATE ALL TABLE ---------------------------#
    
with app.app_context():
    db.create_all()

#------------------------------- HOME ROUTE ---------------------------#

@app.route('/')
def home():
    books = db.session.query(Books).all()
    return render_template('index.html', books = books)

#------------------------------- ADD BOOK ROUTE ---------------------------#

@app.route("/add", methods=['GET', 'POST'])
def add():
    
    if request.method == 'POST':
       try:
          books = Books(
           title = request.form['title'],
           author = request.form['author'],
           rating = request.form['rating']
          )
    
          db.session.add(books)
          db.session.commit()
          return redirect('/')
       except IntegrityError as e:
          flash("A book with this title already exists. Please use a different title.")
          return redirect('/add')
    
    return render_template('add.html')

#------------------------------- EDIT ROUTE ---------------------------#

@app.route('/edit/<int:index>',  methods=['GET', 'POST'])
def edit(index):
   book_to_update = Books.query.get(index)

   if request.method == 'POST':
       book_to_update.rating = request.form['rating']
       db.session.commit() 
       flash('Rating updated successfull')
       return redirect('/')
   return render_template('edit.html', book =book_to_update )

#------------------------------- DELETE ROUTE ---------------------------#

@app.route('/<int:index>')
def delete(index):
     book_to_delete = Books.query.get(index)
     if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
     books = Books.query.all()
     return render_template('index.html', books=books)
 
 
 
 
if __name__ == "__main__":
    app.run(debug=True)

