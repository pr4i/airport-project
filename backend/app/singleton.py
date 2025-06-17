
class SingletonDB:
    _instance = None

    def __new__(cls, db):
        if cls._instance is None:
            cls._instance = db
        return cls._instance


