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
    
    def toggle_completed(self):
        self.complete = not self.complete 

    @classmethod
    def all(cls,view,search=None):
        select = Todo.select()
        if view == "active":
            select = select.where(Todo.complete == False)
        if view == "complete":
            select = select.where(Todo.complete == True)
        if search:
            select = select.where(Todo.text.ilike("%" + search + "%"))
        return select.order_by(Todo.order)

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