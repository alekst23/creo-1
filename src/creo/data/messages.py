from typing import Optional
import time

class MessageType:
    id: Optional[int]
    thread_id: int
    character_id: Optional[str]  # Ensure character_id is after thread_id
    role: str
    content: str
    created_at: int

    def __init__(self, thread_id: int, role: str, content: str, created_at: int = None, id: int = None, character_id: Optional[str] = None):
        self.id = id
        self.thread_id = thread_id
        self.character_id = character_id  # Initialize the new field
        self.role = role
        self.content = content
        self.created_at = created_at if created_at is not None else int(time.time() * 1000)

    def to_dict(self):
        return {
            'id': self.id,
            'thread_id': self.thread_id,
            'character_id': self.character_id,  # Include in dictionary
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at
        }

    @staticmethod
    def from_dict(data: dict):
        return MessageType(
            id=data.get('id'),
            thread_id=data.get('thread_id'),
            character_id=data.get('character_id'),  # Retrieve from dictionary
            role=data.get('role'),
            content=data.get('content'),
            created_at=data.get('created_at')
        )
    
    @staticmethod
    def from_tuple(data: tuple):
        return MessageType(
            id=data[0],
            thread_id=data[1],
            character_id=data[2] if len(data) > 2 else None,  # Handle tuple conversion
            role=data[3],
            content=data[4],
            created_at=data[5]
        )

class MessageModel:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        self.db.execute('''CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            thread_id TEXT NOT NULL,
                            character_id TEXT,
                            role TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created_at INTEGER NOT NULL
                        )''')

    def add_message(self, message: MessageType):
        with self.db:
            cursor = self.db.execute('''INSERT INTO messages (thread_id, character_id, role, content, created_at)
                                        VALUES (?, ?, ?, ?, ?)''', (message.thread_id, message.character_id, message.role, message.content, message.created_at))
            self.db.commit()
            return cursor.lastrowid

    def get_message_by_id(self, message_id):
        cursor = self.db.execute('''SELECT * FROM messages WHERE id = ?''', (message_id,))
        if row := cursor.fetchone():
            return MessageType.from_tuple(row)
        else:
            return None
        
    def get_messages_by_thread_id(self, thread_id, character_id=None):
        if character_id:
            cursor = self.db.execute('''SELECT * FROM messages WHERE thread_id = ? AND character_id = ?''', (thread_id, character_id))
        else:
            cursor = self.db.execute('''SELECT * FROM messages WHERE thread_id = ?''', (thread_id,))
        return [MessageType.from_tuple(row) for row in cursor.fetchall()]


    def update_message(self, message: MessageType):
        with self.db:
            cursor = self.db.execute('''UPDATE messages SET thread_id = ?, character_id = ?, role = ?, content = ?, created_at = ? WHERE id = ?''',
                            (message.thread_id, message.character_id, message.role, message.content, message.created_at, message.id))
            self.db.commit()
            return cursor.rowcount > 0

    def delete_message(self, message_id):
        with self.db:
            cursor = self.db.execute('''DELETE FROM messages WHERE id = ?''', (message_id,))
            self.db.commit()
            return cursor.rowcount > 0
