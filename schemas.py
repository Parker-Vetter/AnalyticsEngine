from pydantic import BaseModel

class StatSubmit(BaseModel):
    player_id: str
    kills: int