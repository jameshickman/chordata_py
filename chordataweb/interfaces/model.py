"""
Base class for abstracted Models.
Sets up the database instance and connection on the current object.

If database is none, then it is a placeholder instance that doesn't do anything
except be a Controller attribute until replaced with a 'live' instance.

Extend with application specific operation methods.
"""


from chordataweb.interfaces.database import BaseDatabase


class BaseModel:
    def __init__(self, database: BaseDatabase = None, configuration: dict = None):
        if database is None and configuration is None:
            return
        if database is not None:
            self.database = database
            self.connection = database.get_connection()
        if configuration is None:
            self.configuration = {}
        else:
            self.configuration = configuration
        pass
