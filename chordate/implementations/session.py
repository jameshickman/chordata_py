import os
import pickle
import uuid
import time
import glob

"""
Tenant data is a dict where the key is the tenant name and the value is a list of groups
the user has membership in for that tenant.
"""


class SessionManager:
    def __init__(self, cfg):
        self.config = cfg
        self._purge()

    def start(self):
        session_id = uuid.uuid4()
        self.session_write(str(session_id), {})
        return str(session_id)

    def get(self, session_id):
        if not os.path.isfile(os.path.join(self.config['session_path'], str(session_id) + ".bin")):
            return False
        return self._session_read(session_id)

    def end(self, session_id):
        if session_id:
            os.remove(os.path.join(self.config['session_path'], session_id + ".bin"))

    def session_write(self, session_id: str, data: dict):
        fh = open(
            os.path.join(self.config['session_path'], str(session_id) + ".bin"),
            'wb'
        )
        pickle.dump(data, fh)
        fh.close()

    def _session_read(self, session_id):
        fh = open(
            os.path.join(self.config['session_path'], str(session_id) + ".bin"),
            'rb'
        )
        data = pickle.load(fh)
        fh.close()
        return data

    def _purge(self):
        """
        Purge any session files older than the specified expire time
        """
        files = glob.glob(
            os.path.join(self.config['session_path'], "*.bin")
        )
        now = int(time.time())
        for filename in files:
            ftime = int(os.path.getmtime(filename))
            if ftime < now - int(self.config['session_timeout']):
                os.remove(filename)
        return
