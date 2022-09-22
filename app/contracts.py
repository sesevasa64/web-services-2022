from pydantic import BaseModel


class User(BaseModel):
    """Contract for User."""
    name: str
    surname: str
    age: int
