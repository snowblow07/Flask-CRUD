from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# To initialize the database:
# >>> python
# >>> from app import db
# >>> db.create_all()
# >>> exit()


#Create App
app = Flask(__name__)

#Setup DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db" #four slashes for absolute path ////
#Initialize DB
db = SQLAlchemy(app)

#Create a table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    #Method to print name of the object
    def __repr__(self):
        return "<Task %r>" % self.id

#main route
@app.route('/', methods=["POST", "GET"])
def index():
    #return "Hello World!"
    #return render_template("index.html")
    if request.method =='POST':
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        #send new_task to db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task"
    else:
        #
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

#delete route
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

#update route
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]

        #send updated task to db
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"
    else:
        return render_template("update.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
