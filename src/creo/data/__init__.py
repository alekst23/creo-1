from sqlite3 import Connection

from .output import OutputModel
from .input import InputModel
from .messages import MessageModel

class DataModel():
    def __init__(self):
        conn = Connection('data.db')
        self.output = OutputModel(conn)
        self.input = InputModel(conn)
        self.messages = MessageModel(conn)