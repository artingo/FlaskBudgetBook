
class User:
    def __init__(self, firstname: str, lastname: str):
        self.firstname = firstname
        self.lastname = lastname

    @property
    def fullname(self) -> str:
        return f"{self.firstname} {self.lastname}"