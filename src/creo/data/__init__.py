from sqlite3 import Connection

from .thoughts import ThoughtModel, ThoughtType
from .messages import MessageModel, MessageType
from .state import StateModel, StateType
from .output import OutputModel, OutputType
from .input import InputModel, InputType
from .locations import LocationModel, LocationType
from .characters import CharacterModel, CharacterType
from .items import ItemModel, ItemType
#from .items import ItemModel, ItemType

class DataModel():
    def __init__(self):
        conn = Connection('data.db')
        self.thoughts = ThoughtModel(conn)
        self.messages = MessageModel(conn)
        self.state = StateModel(conn)
        self.output = OutputModel(conn)
        self.input = InputModel(conn)
        self.locations = LocationModel(conn)
        self.characters = CharacterModel(conn)
        self.items = ItemModel(conn)
