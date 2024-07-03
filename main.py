from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
# Ensure the password special characters are URL encoded
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} - {self.task}"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    todos = Todo.query.all()
    if request.method == "POST":
        task = request.form["title"]
        desc = request.form["desc"]
        if len(task) == 0 or len(desc) == 0:
            return render_template(
                "index.html", todos=todos, error="Please Enter Valid Filds"
            )
        todo = Todo(task=task, desc=desc)
        db.session.add(todo)
        db.session.commit()
        todos = Todo.query.all()
        return render_template("index.html", todos=todos)

    return render_template("index.html", todos=todos)


@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    if request.method == "POST":
        todo.task = request.form["title"]
        todo.desc = request.form["desc"]
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)
