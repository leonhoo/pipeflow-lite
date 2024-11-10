class BaseError(Exception):
    def __init__(self, message="", tag=""):
        self._message_ = message
        self._tag_ = tag

    def __str__(self):
        return f"{self._message_} {self._tag_}"


class ClassNotFoundError(Exception):
    def __init__(self, tag=""):
        self.message = "Class not found."


class ActionOrderError(Exception):
    def __init__(self, tag=""):
        self.message = "The node order is abnormal."
