
class Session():
    session_id: str
    thread_id: str

    def __init__(self, session_id: str, thread_id: str):
        self.session_id = session_id
        self.thread_id = thread_id