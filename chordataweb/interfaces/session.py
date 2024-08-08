class BaseSessionManager:
    def __init__(self, cfg):
        self.config = cfg
        self._purge()

    def start(self):
        pass

    def get(self, session_id):
        pass

    def end(self, session_id):
        pass

    def session_write(self, session_id: str, data: dict):
        pass

    def _purge(self):
        pass
