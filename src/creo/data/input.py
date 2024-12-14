from typing import Optional
import time

class InputType:
    id: Optional[int]
    thread_id: int
    input: str
    created_at: int

    def __init__(self, thread_id: int, input: str, created_at: int = None, id: int = None):
        self.id = id
        self.thread_id = thread_id
        self.input = input
        self.created_at = created_at if created_at is not None else int(time.time() * 1000)

    def to_dict(self):
        return {
            'id': self.id,
            'thread_id': self.thread_id,
            'input': self.input,
            'created_at': self.created_at
        }

    @staticmethod
    def from_dict(data: dict):
        return InputType(
            id=data.get('id'),
            thread_id=data.get('thread_id'),
            input=data.get('input'),
            created_at=data.get('created_at')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        return InputType(
            id=data[0],
            thread_id=data[1],
            input=data[2],
            created_at=data[3]
        )

class InputModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS inputs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            thread_id INTEGER NOT NULL,
                            input TEXT NOT NULL,
                            created_at INTEGER NOT NULL
                        )''')

    def add_input(self, input: InputType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO inputs (thread_id, input, created_at)
                                        VALUES (?, ?, ?)''', (input.thread_id, input.input, input.created_at))
            self.db.commit()
            return cursor.lastrowid

    def get_input_by_id(self, input_id):
        cursor = self.db.execute('''SELECT * FROM inputs WHERE id = ?''', (input_id,))
        if row := cursor.fetchone():
            return InputType.from_tuple(row)
        else:
            return None
        
    def get_inputs_by_thread_id(self, thread_id):
        cursor = self.db.execute('''SELECT * FROM inputs WHERE thread_id = ?''', (thread_id,))
        inputs = [InputType.from_tuple(row) for row in cursor.fetchall()]
        return inputs

    def update_input(self, input: InputType):
        with self.db:
            cursor = self.db.execute('''UPDATE inputs SET thread_id = ?, input = ?, created_at = ? WHERE id = ?''',
                            (input.thread_id, input.input, input.created_at, input.id))
            self.db.commit()
            return cursor.rowcount > 0

    def delete_input(self, input_id):
        with self.db:
            cursor = self.db.execute('''DELETE FROM inputs WHERE id = ?''', (input_id,))
            self.db.commit()
            return cursor.rowcount > 0
