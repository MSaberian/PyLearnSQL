import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect('todo_list.db')
        self.cursor = self.con.cursor()

    def get_tasks(self):
        query = 'SELECT * FROM tasks'
        result = self.cursor.execute(query)
        tasks = result = result.fetchall()
        return tasks

    def add_new_task(self, new_title, new_description, Priority, Date):
        try:
            query = f'INSERT INTO tasks(title, description, priority, date) VALUES("{new_title}","{new_description}","{Priority}","{Date}")'
            self.cursor.execute(query)
            self.con.commit()
            return True
        except:
            return False
        
    def remove_task(self,id):
        try:
            query = f'DELETE FROM tasks WHERE id = "{id}"'
            self.cursor.execute(query)
            self.con.commit()
            return True
        except:
            return False

        
    def done_task(self,id,checked):
        try:
            if checked:
                checked_int = 1
            else:
                checked_int = 0
            query = f"UPDATE tasks SET is_done='{checked_int}' WHERE id ='{id}'"
            self.cursor.execute(query)
            self.con.commit()
            return True
        except:
            return False