from models.todo import ToDo
from datetime import datetime
import json


class IdNotFound(Exception):
    
    def __init__(self, *args: object, msg = "") -> None:
        super().__init__(*args)
        self.msg = msg

class ToDoList:

    def __init__(self, todos=list(), storage_file_path="todos.json"):
        self.__todos = todos
        self.__storage_file_path = storage_file_path
        if len(todos) == 0:
            self.__read_todos()
        else:
            self.__write_todos()

    @property
    def todos(self):
        return self.__todos.copy()

    def __create_id(self):
        """
        Creates the ID of each todo instance
        """
        if len(self.__todos) == 0:
            return 1
        last_todo = self.__todos[-1]
        return last_todo.todo_id + 1

    def add_todo(self,title, description):
        """
        Adds a todo to the todos_list while generating an Id for it
        """
        todo_id = self.__create_id()
        status = "Pending"
        todo = ToDo(title, description, todo_id, status=status)
        self.__todos.append(todo)
        self.__write_todos()
        print(f"Todo with Id {todo_id} was created.")

    def get_todo_by_id(self,todo_id):
        """
        Searches for a todo in the todos_list with the Id provided as param and returns it.
        If a todo is not found with the provided Id an error IdNotFound is raised
        """
        for todo in self.__todos:
            if todo.todo_id ==todo_id:
                return todo
        raise IdNotFound(msg = f"No ToDo found with ID {todo_id}!")

    def update_todo(self,todo_id,newtitle = None, newdescription = None, newstatus = None):
        """
        Updates a todo by id in the todo_list
        If a todo is not found with the provided Id an error IdNotFound is raised
        """
        try:
            todo = self.get_todo_by_id(todo_id)  
        except IdNotFound as e:
            print(e.msg)
        else:
            if newtitle != None:
                todo.title = newtitle
                print(f"Title was updated on Todo with Id {todo_id}.")
            if newdescription != None:
                todo.description = newdescription
                print(f"Description was updated on Todo with Id {todo_id}.")
            if newstatus != None:
                todo.status = newstatus
                if newstatus.lower().strip() == "done":
                    todo.completion_date = datetime.now().isoformat(timespec="seconds")
                    print(type(todo.completion_date))
                else:
                    todo.completion_date = None
                print(f"Status was updated on Todo with Id {todo_id}.")
            self.__write_todos()
            
    def delete_todo(self, todo_id):
        """
        Deletes a todo by id from the todo_list
        If a todo is not found with the provided Id an error IdNotFound is raised
        """
        try:
            todelete = self.get_todo_by_id(todo_id)
        except IdNotFound as e:
            print(e.msg)
        else:
            self.__todos.remove(todelete)
            self.__write_todos()
            print(f"Todo with ID {todo_id} was deleted")

    def show_todo_by_id(self, todo_id):
        """
        Searches for a todo by id from the todo_list and returns it to the user with all the necessary data
        If a todo is not found with the provided Id an error IdNotFound is raised
        """
        try:
            todo = self.get_todo_by_id(todo_id)
        except IdNotFound as e:
            print(e.msg)
        else:
            todo.print_all()
        
    def __read_todos(self):
        """
        Reades the todos.json file and gets all the todos inside it and append them to the list of todos
        If the file is not found with raise IOError but pass it
        If the file has no data we raise json.decoder.JSONDecodeError and pass it
        """
        try:
            storage = None
            storage = open(self.__storage_file_path, mode="r")
            todos_data = json.load(storage)
            for todo_data in todos_data:
                todo = ToDo(todo_data["title"],
                            todo_data["description"],
                            todo_id=todo_data["todo_id"],
                            create_date=todo_data["create_date"],
                            status=todo_data["status"],
                            completion_date=todo_data["completion_date"])
                self.__todos.append(todo)
        except IOError:
            print("Nu exista")
        except json.decoder.JSONDecodeError:
            pass
        finally:
            storage and storage.close()

    def __write_todos(self):
        """
        Writes the todos from the session in the todos.json file
        If the file is not found with raise IOError and display the message
        """
        try:
            storage = open(self.__storage_file_path, mode="w")
            dict_list = list()
            for todo in self.__todos:
                todo_as_dict = {
                    "todo_id": todo.todo_id,
                    "title": todo.title,
                    "description": todo.description,
                    "create_date": str(todo.create_date),
                    "status": todo.status,
                    "completion_date": str(todo.completion_date)
                    }
                dict_list.append(todo_as_dict)
            json.dump(dict_list, storage)
        except IOError as e:
            print(e.strerror)
        finally:
            storage.close()