#Make a To-Do console app 
#Create To-Do Objects(toDoId-Title-createDate-Description-Status--Pending,In Progress,Done--completionDate)

from datetime import datetime


class ToDo:
    
    def __init__(self, title, description, todo_id=None, create_date=datetime.now().isoformat(timespec="seconds"),status="Pending", completion_date=None):
        self.title = title
        self.description = description
        self.todo_id = todo_id
        self.create_date = create_date
        self.status = status
        self.completion_date = completion_date
    
    def print(self):
        print(f"Id: {self.todo_id},title: {self.title}, created at: {self.create_date.replace('T', ' ')}, status: {self.status}")
    
    def print_all(self):
        print(f"Id: {self.todo_id},\n", 
              f"Title: {self.title},\n",
              f"Description: {self.description},\n",
              f"Created date: {self.create_date.replace('T', ' ')},\n",
              f"Status: {self.status},\n",
              f"Completion date: {self.completion_date and self.completion_date.replace('T',' ')}")
    
    

 