from typing import Optional
import time

class OutputType:
    id: Optional[int]
    thread_id: int
    output: str
    created_at: int

    def __init__(self, thread_id: int, output: str, created_at: int = None, id: int = None):
        self.id = id
        self.thread_id = thread_id
        self.output = output
        self.created_at = created_at if created_at is not None else int(time.time() * 1000)

    def to_dict(self):
        return {
            'id': self.id,
            'thread_id': self.thread_id,
            'output': self.output,
            'created_at': self.created_at
        }

    @staticmethod
    def from_dict(data: dict):
        return OutputType(
            id=data.get('id'),
            thread_id=data.get('thread_id'),
            output=data.get('output'),
            created_at=data.get('created_at')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        return OutputType(
            id=data[0],
            thread_id=data[1],
            output=data[2],
            created_at=data[3]
        )

class OutputModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS outputs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            thread_id INTEGER NOT NULL,
                            output TEXT NOT NULL,
                            created_at INTEGER NOT NULL
                        )''')

    def add_output(self, output: OutputType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO outputs (thread_id, output, created_at)
                                        VALUES (?, ?, ?)''', (output.thread_id, output.output, output.created_at))
            self.db.commit()
            return cursor.lastrowid

    def get_output_by_id(self, output_id):
        cursor = self.db.execute('''SELECT * FROM outputs WHERE id = ?''', (output_id,))
        if row := cursor.fetchone():
            return OutputType.from_tuple(row)
        else:
            return None
        
    def get_outputs_by_thread_id(self, thread_id):
        cursor = self.db.execute('''SELECT * FROM outputs WHERE thread_id = ?''', (thread_id,))
        outputs = [OutputType.from_tuple(row) for row in cursor.fetchall()]
        return outputs

    def update_output(self, output: OutputType):
        with self.db:
            cursor = self.db.execute('''UPDATE outputs SET thread_id = ?, output = ?, created_at = ? WHERE id = ?''',
                            (output.thread_id, output.output, output.created_at, output.id))
            self.db.commit()
            return cursor.rowcount > 0

    def delete_output(self, output_id):
        with self.db:
            cursor = self.db.execute('''DELETE FROM outputs WHERE id = ?''', (output_id,))
            self.db.commit()
            return cursor.rowcount > 0
