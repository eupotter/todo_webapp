from flask import Flask, render_template, request, redirect, url_for
from models.todo_list import ToDoList

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/todos_list")
def todos_list():
    todo_list = ToDoList()
    return render_template("todo_list.html", todos=todo_list.todos)

@app.route("/create_todo",methods=["GET","POST"])
def create_todo():
    if request.method == "GET":
        return render_template("create_todo.html")
    todos_list = ToDoList()
    todo_data = request.form
    print(todo_data)
    todos_list.add_todo(todo_data["title"],todo_data["description"])
    return redirect(url_for("todos_list"))

@app.route("/mark_done/<int:todo_id>")
def mark_done(todo_id):
    todos_list = ToDoList()
    todos_list.update_todo(todo_id, newstatus="Done")
    return redirect(url_for("todos_list"))

@app.route("/delete_todo/<int:todo_id>")
def delete_todo(todo_id):
    todos_list = ToDoList()
    todos_list.delete_todo(todo_id)
    return redirect(url_for("todos_list"))

@app.route("/edit_todo/<int:todo_id>", methods=["GET","POST"])
def edit_todo(todo_id):
    todos_list = ToDoList()
    todo = todos_list.get_todo_by_id(todo_id)
    if request.method == "GET":
        return render_template("edit_todo.html", todo=todo)
    todo_data = request.form
    todos_list.update_todo(todo_id, newtitle=todo_data["title"], newdescription=todo_data["description"], newstatus=todo_data["status"])
    return redirect(url_for("todos_list"))

if __name__ == "__main__":
    app.run()