from flask import Flask, request, render_template, redirect, jsonify
from src.model.todo import Todo, db
from playhouse.migrate import *
from datetime import datetime

app = Flask(__name__, static_url_path='', static_folder='static')

# Function to perform database migration
def run_migration():
    migrator = SqliteMigrator(db)
    try:
        migrate(
            migrator.add_column('todo', 'due_date', DateField(null=True))
        )
        print("Migration completed: Added 'due_date' column.")
    except Exception as e:
        print(f"Migration error: {e}")

# Perform migration before creating tables
run_migration()

with db:
        db.create_tables([Todo])
    
@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@app.route('/')
def index():
    view = request.args.get("view", "all")
    search = request.args.get("search", None)
    sort_by_due_date = request.args.get("sort", "") == "due_date"
    todos = Todo.all(view=view, search=search, sort_by_due_date=sort_by_due_date)
    return render_template("index.html", todos=todos, view=view, sort_by_due_date=sort_by_due_date)



@app.get('/todos')
def all_todos():
    view = request.args.get('view',None)
    search = request.args.get('search',None)
    todos = Todo.all(view, search)
    return render_template("index.html",todos=todos, view=view, search=search)


@app.get('/search')
def search():
    view = request.args.get('view',None)
    search = request.args.get('search',None)
    todos = Todo.all(view, search)
    return render_template("todos.html",todos=todos, view=view, search=search)


@app.post('/todos')
def create_todo():
    view = request.form.get('view',None)
    due_date_str = request.form.get('due_date', None)
    due_date = due_date_str if due_date_str else None
    todo = Todo(text=request.form['todo'], complete=False, due_date=due_date)
    todo.save()
    return redirect("/todos" + addViewFilter(view))


@app.post('/todos/<id>/toggle')
def toggle_todo(id):
    view = request.form.get('view',None)
    todo = Todo.find(int(id))
    todo.toggle_completed() 
    todo.save()
    todos = Todo.all(view)
    return render_template("main.html",todos=todos, view=view, editing=None)


@app.get('/todos/<id>/edit')
def edit(id):
    view = request.args.get('view',None)
    todos = Todo.all(view)
    return render_template("index.html", todos=todos, editing=int(id), view=view)


@app.post('/todos/<id>')
def update_todo(id):
    view = request.form.get('view',None)
    todo = Todo.find(int(id))
    todo.text = request.form['todo']
    due_date_str = request.form.get('due_date', None)
    todo.due_date = due_date_str if due_date_str else None
    todo.save()
    return redirect("/todos" + addViewFilter(view))


@app.get('/todos/reorder')
def showReorderUI():
    view = request.args.get('view',None)
    todos = Todo.all(view)
    return render_template("reorder.html",todos=todos)


@app.post('/todos/reorder')
def updateTodoOrder():
    view = request.args.get('view',None)
    id_list = request.form.getlist("ids")
    Todo.reorder(id_list)
    todos = Todo.all(view)
    return render_template("main.html",todos=todos, view=view, editing=None)


def addViewFilter(view):
    return (("?view=" + view) if view is not None else "")


@app.route('/calendar')
def calendar():
    todos = Todo.select().where(Todo.due_date.is_null(False)).order_by(Todo.due_date)
    now = datetime.now().date()
    return render_template('calendar.html', todos=todos, now=now)


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    try:
        # Find the todo by its ID
        todo_to_delete = Todo.get(Todo.id == id)
        # Delete the todo from the database
        todo_to_delete.delete_instance()
        return '', 200  # Blank response to delete the item from the DOM
    except DoesNotExist:
        return jsonify({"error": "Todo not found"}), 404


if __name__ == '__main__':
    app.run(port=5000)

