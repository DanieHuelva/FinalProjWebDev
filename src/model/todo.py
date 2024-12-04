from peewee import *
import logging

db = SqliteDatabase('todos.db')

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Todo(Model):
    text = CharField()
    complete = BooleanField()
    order = IntegerField(null=True)
    due_date = DateField(null=True)  # Add the due_date field
    
    def toggle_completed(self):
        self.complete = not self.complete 

    @classmethod
    def all(cls,view,search=None, sort_by_due_date=False):
        select = Todo.select()
        if view == "active":
            select = select.where(Todo.complete == False)
        if view == "complete":
            select = select.where(Todo.complete == True)
        if search:
            select = select.where(Todo.text.ilike("%" + search + "%"))
        if sort_by_due_date:
            select = select.order_by(SQL('COALESCE(due_date, "9999-12-31")').asc())  # Using COALESCE to treat null dates as very far in the future
        else:
            select = select.order_by(Todo.order)
        return select

    @classmethod
    def find(cls,todoID):
        return  Todo.get(Todo.id == todoID)

    
    @classmethod
    def reorder(cls, id_list):
        i = 0
        for tid in id_list:
            todo = Todo.find(int(tid))
            todo.order = i
            i = i + 1
            todo.save()
            
    class Meta:
        database = db